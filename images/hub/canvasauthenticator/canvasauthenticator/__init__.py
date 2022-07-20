from traitlets import List, Unicode, default
from oauthenticator.generic import GenericOAuthenticator
import aiohttp

class CanvasOAuthenticator(GenericOAuthenticator):
    """
    Canvas OAuth2 based authenticator for JupyterHub.

    Collects info about user & enrolled courses from canvas,
    puts them into auth_state. To refresh, user has to re-login.
    """

    strip_email_domain = Unicode(
        '',
        config=True,
        help="""
        Strip this domain from user emails when making their JupyterHub user name.

        For example, if almost all your users have emails of form username@berkeley.edu,
        you can set this to 'berkeley.edu'. A canvas user with email yuvipanda@berkeley.edu
        will get a JupyterHub user name of 'yuvipanda', while a canvas user with email
        yuvipanda@gmail.com will get a JupyterHub username of 'yuvipanda@gmail.com'.

        By default, *no* domain stripping is performed, and the JupyterHub username
        is the primary email of the canvas user.
        """
    )

    canvas_url = Unicode(
        '',
        config=True,
        help="""
        URL to canvas installation to use for authentication.

        Must have a trailing slash
        """
    )

    canvas_course_key = Unicode(
        '',
        config=True,
        help="""
        Key to lookup course identifier from Canvas course data.
        See https://canvas.instructure.com/doc/api/courses.html.

        This might be 'sis_course_id', 'course_code', 'id', etc.

        sis_course_id examples: CRS:MATH-98-2021-C, CRS:CHEM-1A-2021-D, CRS:PHYSICS-77-2022-C
        course_code examples: "Math 98", "Chem 1A Fall 2021", "PHYSICS 77-LEC-001"
        """
    )

    @default('canvas_course_code')
    def _default_canvas_course_key(self):
        """
        The default is 'course_code' because it should contain human-readable
        information, it cannot be overridden by nicknames, and the user won't be
        excluded from reading it, unlike the possibility of some sis_ attributes.
        """
        return 'course_code'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.canvas_url:
            raise ValueError('c.CanvasOAuthenticator.canvas_url must be set')

        # canvas_url must have a trailing slash
        if self.canvas_url[-1] != '/':
            raise ValueError('c.CanvasOAuthenticator.canvas_url must have a trailing slash')

        self.token_url = f'{self.canvas_url}login/oauth2/token'
        self.userdata_url = f'{self.canvas_url}api/v1/users/self/profile'

        self.extra_params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            # We set replace_tokens=1 to prevent tokens from accumulating.
            # https://github.com/instructure/canvas-lms/blob/release/2022-08-03.12/spec/controllers/oauth2_provider_controller_spec.rb#L520
            'replace_tokens': 1,
        }

    async def get_canvas_items(self, token, url):
        """
        Get paginated items from Canvas.
        https://canvas.instructure.com/doc/api/file.pagination.html
        """
        headers = dict(Authorization = f"Bearer {token}")
        data = []

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=self.extra_params) as r:
                if r.status != 200:
                    raise Exception(f"error fetching items for {self.username}: {url} -- {r.status} -- {r.text()}")
                data = await r.json()
                if 'next' in r.links.keys():
                    url = r.links['next']['url']
                    data += await self.get_canvas_items(token, url)

        return data

    async def get_courses(self, token):
        """
        Get list of courses enrolled by the current user

        See https://canvas.instructure.com/doc/api/courses.html#method.courses.index
        """
        url = f"{self.canvas_url}/api/v1/courses"

        data = await self.get_canvas_items(token, url)

        return data

    def format_group(course_identifier, enrollment_type):
        if enrollment_type is None:
            return f'canvas::{course_identifier}'
        else:
            return f'canvas::{course_identifier}::{enrollment_type}'

    def extract_course_groups(courses):
        '''
        Extract course identifiers for each course the user is enrolled in
        and format them as group names.
        '''
        groups = []

        for course in user['auth_state']['courses']:
            course_id = course.get(self.course_key, None)
            if course_id is None:
                continue

            # examples: [{'enrollment_state': 'active', 'role': 'TeacherEnrollment', 'role_id': 1773, 'type': 'teacher', 'user_id': 12345}],
            # https://canvas.instructure.com/doc/api/courses.html#method.courses.index
            # there may be multiple enrollments per course
            enrollment_types = list(
                map(
                    lambda x: x.get('type', None), course.get('enrollments', [])
                )
            )

            for enrollment_type in enrollment_types:
                groups.append(format_group(course_id, enrollment_type))

        return groups

    async def authenticate(self, handler, data=None):
        """
        Augment base user auth info with course info
        """
        user = await super().authenticate(handler, data)
        courses = await self.get_courses(user['auth_state']['access_token'])
        user['auth_state']['courses'] = courses
        user['groups'] = self.extract_course_groups(courses)

        return user

    def normalize_username(self, username):
        username = username.lower()
        # To make life easier & match usernames with existing users who were
        # created with google auth, we want to strip the domain name. If not,
        # we use the full email as the official user name
        if self.strip_email_domain and username.endswith('@' + self.strip_email_domain):
            return username.split('@')[0]
        return username

    async def pre_spawn_start(self, user, spawner):
        """Pass oauth data to spawner via OAUTH2_ prefixed env variables."""
        auth_state = yield user.get_auth_state()
        if not auth_state:
            return
        if 'access_token' in auth_state:
            spawner.environment["OAUTH2_ACCESS_TOKEN"] = auth_state['access_token']
        # others are lti_user_id, id, integration_id
        if 'oauth_user' in auth_state:
            for k in ['login_id', 'name', 'sortable_name', 'primary_email']:
                if k in auth_state['oauth_user']:
                    spawner.environment[f"OAUTH2_{k.upper()}"] = auth_state['oauth_user'][k]

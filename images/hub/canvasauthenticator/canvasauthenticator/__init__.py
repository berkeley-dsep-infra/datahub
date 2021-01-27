from traitlets import List, Unicode
from oauthenticator.generic import GenericOAuthenticator
import aiohttp

class CanvasAuthenticator(GenericOAuthenticator):
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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.canvas_url:
            raise ValueError('c.CanvasAuthenticator.canvas_url must be set')

        # canvas_url must have a trailing slash
        if self.canvas_url[-1] != '/':
            raise ValueError('c.CanvasAuthenticator.canvas_url must have a trailing slash')

        self.token_url = f'{self.canvas_url}login/oauth2/token'
        self.userdata_url = f'{self.canvas_url}api/v1/users/self/profile'

        self.extra_params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

    async def get_courses(self, token):
        """
        Get list of courses enrolled by the current user
        """
        headers = dict(Authorization = f"Bearer {token}")
        url = f"{self.canvas_url}/api/v1/courses"
        data = []

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=self.extra_params) as r:
                if r.status != 200:
                    raise Exception(f"error fetching course info for {self.username}: {r.status} -- {r.text()}")
                data = await r.json()
        return data

    async def authenticate(self, handler, data=None):
        """
        Augment base user auth info with course info
        """
        user = await super().authenticate(handler, data)
        user['auth_state']['courses'] = await self.get_courses(
            user['auth_state']['access_token']
        )
        print(user)
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

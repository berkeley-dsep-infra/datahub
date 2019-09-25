from traitlets import List, Unicode
from oauthenticator.generic import GenericOAuthenticator
from tornado import gen

canvas_site = 'https://ucberkeley.test.instructure.com/'

class CanvasAuthenticator(GenericOAuthenticator):

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

    def normalize_username(self,username):
        username = username.lower()
        # To make life easier & match usernames with existing users who were
        # created with google auth, we want to strip the domain name. If not,
        # we use the full email as the official user name
        if self.strip_email_domain and username.endswith('@' + self.strip_email_domain):
            return username.split('@')[0]
        return username

    @gen.coroutine
    def pre_spawn_start(self, user, spawner):
        """Pass oauth data to spawner via OAUTH2_ prefixed env variables."""
        auth_state = yield user.get_auth_state()
        return if not auth_state
        for k in ['access_token', 'oauth_user']:
            if k in auth_state:
                spawner.environment[f"OAUTH2_{k.upper()}"] = auth_state[k]

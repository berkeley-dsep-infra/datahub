from traitlets import List, Unicode
from oauthenticator.generic import GenericOAuthenticator
from tornado import gen

canvas_site = 'https://ucberkeley.test.instructure.com/'

class CanvasAuthenticator(GenericOAuthenticator):

    allowed_email_domains = List(
        [],
        config=True,
        help="""
        List of domains whose users are authorized to log in.

        This relies on the primary email id set in canvas for the user
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
        # FIXME: allow 
        username = username.split('@')[0]
        return username
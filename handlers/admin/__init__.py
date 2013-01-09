from webapp2 import Route
from webapp2_extras import routes

import base
import scribes
import account

__all__ = [
    'base',
    'scribes',
    'account',
]

routes = [
    routes.PathPrefixRoute(r'/<scribetype:(lore|about)>', scribes.routes),
    routes.PathPrefixRoute(r'/account', account.routes),
]

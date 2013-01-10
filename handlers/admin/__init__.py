from webapp2 import Route
from webapp2_extras import routes

import base
import scribes
import account
import character

__all__ = [
    'base',
    'scribes',
    'account',
    'character',
]

routes = [
    routes.PathPrefixRoute(r'/<scribetype:(lore|about)>', scribes.routes),
    routes.PathPrefixRoute(r'/account', account.routes),
    routes.PathPrefixRoute(r'/character', character.routes),
]

from webapp2_extras import routes

import base
import scribes
import account
import character
import forums

__all__ = [
    'base',
    'scribes',
    'account',
    'character',
    'forums',
]

routes = [
    routes.PathPrefixRoute(r'/<scribetype:(lore|about)>', scribes.routes),
    routes.PathPrefixRoute(r'/account', account.routes),
    routes.PathPrefixRoute(r'/character', character.routes),
    routes.PathPrefixRoute(r'/forums', forums.routes),
]

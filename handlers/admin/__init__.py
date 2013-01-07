from webapp2 import Route
from webapp2_extras import routes

__all__ = [
  'base',
  'scribes',
]

import scribes
import account

routes = [
    routes.PathPrefixRoute(r'/<scribetype:(lore|about)>', scribes.routes),
    routes.PathPrefixRoute(r'/account', account.routes),
]

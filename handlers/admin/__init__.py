from webapp2 import Route
from webapp2_extras import routes

__all__ = [
  'base',
  'scribes',
]

import scribes

routes = [
    routes.PathPrefixRoute(r'/<scribetype:(lore|about)>', scribes.routes),
]

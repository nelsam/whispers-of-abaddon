import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from webapp2 import Route, WSGIApplication
from webapp2_extras import routes

import settings
import handlers

mapping = [
    Route(r'/', handlers.simple.Home, name='home'),
    Route(r'/about', handlers.simple.About, name='about'),
    Route(r'/lore', handlers.simple.Lore, name='lore'),
    routes.PathPrefixRoute(r'/account', handlers.account.routes),
    #Route(r'/static/<path:.*>', handlers.base.StaticHandler,
    #              name='static'),
    routes.PathPrefixRoute(r'/<:(admin|system)>', handlers.admin.routes),
    ]

debug = not settings.is_production()
application = WSGIApplication(mapping, debug=debug)


def main():
    application.run()

if __name__ == '__main__':
    main()

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import webapp2
from webapp2_extras import routes

import settings
import handlers

mapping = [
    webapp2.Route(r'/', handlers.simple.Home, name='home'),
    webapp2.Route(r'/about', handlers.simple.About, name='about'),
    webapp2.Route(r'/lore', handlers.simple.Lore, name='lore'),
    #webapp2.Route(r'/static/<path:.*>', handlers.base.StaticHandler,
    #              name='static'),
    ]

debug = not settings.is_production()
application = webapp2.WSGIApplication(mapping, debug=debug)


def main():
    application.run()

if __name__ == '__main__':
    main()

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import webapp2
from webapp2_extras import routes

import handlers

def main():
    mapping = [
        webapp2.Route(r'/', handlers.home.Home, name='home'),
        ]

    debug = not settings.is_production()
    application = webapp2.WSGIApplication(mapping, debug=debug)

    application.run()

if __name__ == '__main__':
    main()

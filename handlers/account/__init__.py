# -*- coding: utf-8 -*-

__all__ = []

from webapp2 import Route
from webapp2_extras import routes

import preferences
import character
import communication

routes = [
    Route('/', preferences.Account, name='account'),
    Route('/edit', preferences.AccountEdit, name='account-edit'),
    routes.PathPrefixRoute('/character', character.routes),
    routes.PathPrefixRoute('/inbox', communication.routes),
]

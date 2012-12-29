from webapp2 import Route

__all__ = [
  'base',
  'scribes',
]

import scribes

routes = [
    Route(r'/lore', scribes.lore.List, name="admin-lore-list"),
    Route(r'/lore/create', scribes.lore.Create, name="admin-lore-create"),
    Route(r'/lore/edit/<entrykey>', scribes.lore.Edit, name="admin-lore-edit"),
    Route(r'/lore/delete/<entrykey>', scribes.lore.Delete, name="admin-lore-delete"),
]

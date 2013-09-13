# -*- coding: utf-8 -*-

from uvclight import name, implementer
from zope.interface import Interface
from dolmen.menu import Menu


class ContextualActions(Menu):
    name('contextual')

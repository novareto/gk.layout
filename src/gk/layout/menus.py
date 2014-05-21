# -*- coding: utf-8 -*-

from uvclight import name, get_template
from dolmen.menu import Menu


class ContextualActions(Menu):
    name('contextual')
    template = get_template('contextual.pt', __file__)

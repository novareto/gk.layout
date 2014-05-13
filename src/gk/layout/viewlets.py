# -*- coding: utf-8 -*-

from gatekeeper.app import GateKeeper
from uvclight import context, order, Viewlet, viewletmanager

from .layout import Top
from .menus import ContextualActions


class ContextualMenuDisplay(Viewlet):
    viewletmanager(Top)
    order(20)

    def update(self):
        self.menu = ContextualActions(self.context, self.request, self.view)
        self.menu.update()

    def render(self):
        return self.menu.render()


class Alerts(Viewlet):
    viewletmanager(Top)
    order(15)
    context(GateKeeper)

    def render(self):
        return '<br />'.join(self.context.get_messages())

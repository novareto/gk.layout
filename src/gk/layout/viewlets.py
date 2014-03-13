# -*- coding: utf-8 -*-

from cromlech.browser import slot
from dolmen.viewlet import order, Viewlet
from gatekeeper.app import GateKeeper
from gatekeeper.login import LoginRoot
from uvclight import context
from .layout import Top
from .menus import ContextualActions


class ContextualMenuDisplay(Viewlet):
    slot(Top)
    order(20)

    def update(self):
        self.menu = ContextualActions(self.context, self.request, self.view)
        self.menu.update()

    def render(self):
        return self.menu.render()


class Alerts(Viewlet):
    slot(Top)
    order(15)
    context(GateKeeper)

    def render(self):
        return '<br />'.join(self.context.get_messages())


class LoginAlerts(Viewlet):
    slot(Top)
    order(15)
    context(LoginRoot)

    def render(self):
        return '<br />'.join(self.context.get_messages())

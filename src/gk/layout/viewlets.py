# -*- coding: utf-8 -*-

from gatekeeper.app import GateKeeper
from gk.login.models import LoginRoot
from uvclight import get_template, context, order, Viewlet, viewletmanager

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
    template = get_template('messages.pt', __file__)



class LoginAlerts(Viewlet):
    viewletmanager(Top)
    order(15)
    context(LoginRoot)
    template = get_template('messages.pt', __file__)

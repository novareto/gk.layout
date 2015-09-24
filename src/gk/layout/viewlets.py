# -*- coding: utf-8 -*-

from gatekeeper.app import GateKeeper
from gk.login.models import LoginRoot
from uvclight import Viewlet
from uvclight import get_template, layer, context, order, viewletmanager
from .layout import Top
from .menus import ContextualActions
from . import i18n as _, DefaultLayer


class ContextualMenuDisplay(Viewlet):
    viewletmanager(Top)
    order(20)
    layer(DefaultLayer)

    def update(self):
        self.menu = ContextualActions(self.context, self.request, self.view)
        self.menu.update()

    def render(self):
        return self.menu.render()


class Alerts(Viewlet):
    viewletmanager(Top)
    order(15)
    context(GateKeeper)
    layer(DefaultLayer)

    template = get_template('messages.pt', __file__)


class LoginAlerts(Viewlet):
    viewletmanager(Top)
    order(15)
    context(LoginRoot)
    layer(DefaultLayer)

    template = get_template('messages.pt', __file__)

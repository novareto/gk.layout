# -*- coding: utf-8 -*-

from cromlech.browser import slot
from dolmen.location import get_absolute_url
from dolmen.viewlet import order, Viewlet
from gatekeeper.admin import AdminRoot, MessagesRoot
from gatekeeper.app import GateKeeper
from grokcore.security import require
from uvclight import context, get_template
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

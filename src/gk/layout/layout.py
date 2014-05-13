# -*- coding: utf-8 -*-

from dolmen.message import receive
from uvclight import Layout, ViewletManager, context, get_template
from zope.interface import Interface
from .resources import styles


class Top(ViewletManager):
    context(Interface)


class Footer(ViewletManager):
    context(Interface)


class GateLayout(Layout):
    context(Interface)

    template = get_template('layout.pt', __file__)

    title = u"Gatekeeper"

    def __call__(self, content, **namespace):
        styles.need()
        namespace['user'] = self.request.environment.get('REMOTE_USER')
        namespace['gatekeeper_messages'] = list(receive())
        return Layout.__call__(self, content, **namespace)

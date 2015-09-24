# -*- coding: utf-8 -*-

from dolmen.message import receive
from uvclight import Layout, ViewletManager, context, layer, get_template
from zope.interface import Interface
from .resources import styles
from . import DefaultLayer


class Top(ViewletManager):
    context(Interface)
    layer(DefaultLayer)


class Footer(ViewletManager):
    context(Interface)
    layer(DefaultLayer)


class GateLayout(Layout):
    context(Interface)
    layer(DefaultLayer)

    title = u"Gatekeeper"
    template = get_template('layout.pt', __file__)

    def __call__(self, content, **namespace):
        styles.need()
        namespace['user'] = self.request.environment.get('REMOTE_USER')
        namespace['gatekeeper_messages'] = list(receive())
        return Layout.__call__(self, content, **namespace)

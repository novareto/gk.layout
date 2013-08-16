# -*- coding: utf-8 -*-

from cromlech.webob import response
from dolmen.layout import Layout
from dolmen.message import receive
from grokcore.component import context
from js.bootstrap import bootstrap
from uvclight import get_template
from zope.interface import Interface


class GateLayout(Layout):
    context(Interface)

    responseFactory = response.Response
    template = get_template('layout.pt', __file__)

    title = u"Gatekeeper"
     
    def __call__(self, content, **namespace):
        bootstrap.need()
        namespace['gatekeeper_messages'] = list(receive())
        return Layout.__call__(self, content, **namespace)

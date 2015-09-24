# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

i18n = MessageFactory("gk.layout")


from cromlech.browser.interfaces import ITypedRequest
from dolmen.clockwork.formatters import (
    DefaultFormDateManager,
    DefaultFormDatetimeManager,
    DefaultFormTimeManager
)


class MyDefaultFormDateManager(DefaultFormDateManager):
    size = "medium"


class MyDefaultFormDatetimeManager(DefaultFormDatetimeManager):
    size = "medium"


class MyDefaultFormTimeManager(DefaultFormTimeManager):
    size = "medium"


class DefaultLayer(ITypedRequest):
    """Default Layer for GateKeeper
    """

# -*- coding: utf-8 -*-

from cromlech.browser import 
from grokcore.component import global_utility
from uvclight import implementer, context, get_template, View
from zope.interface import Interface


class Timeout(View):
    context(Interface)
    template = get_template('timeout.pt', __file__)


class Unauthorized(View):
    context(Interface)
    template = get_template('unauthorized.pt', __file__)

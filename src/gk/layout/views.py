# -*- coding: utf-8 -*-

from uvclight import context, get_template, View
from zope.interface import Interface


class Timeout(View):
    context(Interface)
    template = get_template('timeout.pt', __file__)


class Unauthorized(View):
    context(Interface)
    template = get_template('unauthorized.pt', __file__)

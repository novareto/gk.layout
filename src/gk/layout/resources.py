# -*- coding: utf-8 -*-

from fanstatic import Library, Resource
from js.bootstrap import bootstrap

library = Library('gatekeeper', 'static')
styles = Resource(Library, 'gk.css', depends=[bootstrap])

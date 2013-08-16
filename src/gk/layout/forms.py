# -*- coding: utf-8 -*-

from gatekeeper.login import BaseLoginForm
from cromlech.webob import Response
from uvclight import get_template


class LoginForm(BaseLoginForm):
    responseFactory = Response
    template = get_template('form.pt', __file__)

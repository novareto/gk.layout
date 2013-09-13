# -*- coding: utf-8 -*-

from cromlech.sqlalchemy import get_session
from cromlech.webob import Response, Request
from dolmen.content import schema
from dolmen.forms.base import apply_data_event
from dolmen.forms.base import action, Action, Actions, Fields, SuccessMarker
from dolmen.forms.ztk import InvariantsValidation
from dolmen.location import get_absolute_url
from dolmen.message.utils import send
from dolmen.menu import menuentry
from dolmen.view import query_view, make_layout_response
from gatekeeper.admin import IMessage, Message, MessagesRoot, AdminRoot
from gatekeeper.login import BaseLoginForm
from grokcore.component import title, context, name, adapts, MultiAdapter
from grokcore.security import require
from uvclight import get_template, Form
from zope.cachedescriptors.property import CachedProperty
from zope.interface import Interface, implementer

from .menus import ContextualActions
from .resources import gkdate


class LoginForm(BaseLoginForm):
    responseFactory = Response
    template = get_template('form.pt', __file__)


@menuentry(ContextualActions)
class AddForm(Form):
    """A very generic add form.
    """
    name('add')
    context(MessagesRoot)
    title(u"Add")
    require('zope.Public')
    
    fields = Fields(IMessage).omit('id')
    responseFactory = Response
    dataValidators = [InvariantsValidation]
    make_response = make_layout_response

    @property
    def action_url(self):
        return self.request.url

    def updateForm(self):
        gkdate.need()
        self.fields['enable'].strict_format = '%d/%m/%Y %H:%M'
        self.fields['disable'].strict_format = '%d/%m/%Y %H:%M'
        Form.updateForm(self)

    @action(u"Add")
    def add(self):
        data, errors = self.extractData()
        if errors:
            return FAILURE

        item = self.context.model(**data)
        self.context.add(item)
        send(u"Content created.")
        url = get_absolute_url(self.context, self.request)
        return SuccessMarker('Created', True, url=url)
        

@menuentry(ContextualActions)
class EditForm(Form):
    """A very generic add form.
    """
    name('index')
    context(Message)
    title(u"Edit")
    require('zope.Public')

    ignoreContent = False
    ignoreRequest = True
    fields = Fields(IMessage)
    responseFactory = Response
    dataValidators = [InvariantsValidation]
    make_response = make_layout_response

    @property
    def action_url(self):
        return self.request.url

    def updateForm(self):
        gkdate.need()
        self.fields['enable'].strict_format = '%d/%m/%Y %H:%M'
        self.fields['disable'].strict_format = '%d/%m/%Y %H:%M'
        Form.updateForm(self)
        
    @action(u"Update")
    def Update(self):
        data, errors = self.extractData()
        if errors:
            self.submissionError = errors
            return FAILURE

        session = self.context.__parent__.session
        apply_data_event(self.fields, self.context, data)
        session.add(self.context)

        send(u"Mise à jour effectuée.")
        url = get_absolute_url(self.context, self.request)
        return SuccessMarker('Updated', True, url=url)

# -*- coding: utf-8 -*-

from dolmen.forms.base import apply_data_event
from dolmen.forms.ztk import InvariantsValidation
from dolmen.location import get_absolute_url
from dolmen.message.utils import send

from gatekeeper.admin import IMessage, Message, MessagesRoot
from gatekeeper.login import BaseLoginForm

from uvclight import get_template, Form, action, Fields
from uvclight import SuccessMarker, SUCCESS, FAILURE
from uvclight import title, context, name, require, menuentry

from .menus import ContextualActions
from .resources import gkdate


class LoginForm(BaseLoginForm):
    template = get_template('form.pt', __file__)


@menuentry(ContextualActions)
class AddForm(Form):
    """A very generic add form.
    """
    name('add')
    title(u"Add")
    require('zope.Public')
    context(MessagesRoot)
    
    fields = Fields(IMessage).omit('id')
    dataValidators = [InvariantsValidation]

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
    title(u"Edit")
    require('zope.Public')
    context(Message)
    
    ignoreContent = False
    ignoreRequest = True
    fields = Fields(IMessage)
    dataValidators = [InvariantsValidation]

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

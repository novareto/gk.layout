# -*- coding: utf-8 -*-

from dolmen.forms.base import apply_data_event
from dolmen.forms.ztk import InvariantsValidation
from dolmen.location import get_absolute_url
from dolmen.message.utils import send

from gatekeeper.admin import IMessage, Message, MessagesRoot, ON_DATES
from gatekeeper.login import BaseLoginForm

from uvclight import get_template, Form, action, Fields
from uvclight import SuccessMarker, SUCCESS, FAILURE
from uvclight import title, context, name, menuentry
from uvclight.auth import require

from .menus import ContextualActions
from .resources import gkdate
from . import i18n as _


class LoginForm(BaseLoginForm):
    pass


@menuentry(ContextualActions)
class AddForm(Form):
    """A very generic add form.
    """
    name('add')
    title(_(u"add_message", default=_(u"Add message")))
    require('zope.Public')
    context(MessagesRoot)

    fields = Fields(IMessage).omit('id')
    dataValidators = [InvariantsValidation]

    @property
    def action_url(self):
        return self.request.url

    def updateForm(self):
        gkdate.need()
        self.fields['enable'].strict_format = '%d/%m/%y %H:%M'
        self.fields['disable'].strict_format = '%d/%m/%y %H:%M'
        Form.updateForm(self)

    @action(_(u"Add"))
    def add(self):
        data, errors = self.extractData()
        if errors:
            return FAILURE

        if data['activation'] != ON_DATES:
            del data['enable']
            del data['disable']
    
        item = self.context.model(**data)
        self.context.add(item)
        send(_(u"Content created."))
        url = get_absolute_url(self.context, self.request)
        return SuccessMarker('Created', True, url=url)


@menuentry(ContextualActions)
class EditForm(Form):
    """A very generic add form.
    """
    name('index')
    title(_(u"edit_message", default=u"Edit message"))
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

    @action(_(u"Update"))
    def Update(self):
        data, errors = self.extractData()
        if errors:
            self.submissionError = errors
            return FAILURE

        session = self.context.__parent__.session
        apply_data_event(self.fields, self.context, data)
        session.add(self.context)

        send(_(u"Your contents get updated."))
        url = get_absolute_url(self.context, self.request)
        return SuccessMarker('Updated', True, url=url)

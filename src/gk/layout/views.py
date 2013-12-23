# -*- coding: utf-8 -*-

from cromlech.webob import Response
from cromlech.sqlalchemy import get_session
from dolmen.forms.base import DISPLAY, action, SuccessMarker
from dolmen.forms.base import Field, Fields, Actions, Action
from dolmen.forms.base.utils import apply_data_event
from dolmen.forms.table import TableForm, TableActions
from dolmen.location import get_absolute_url
from dolmen.message.utils import send
from gatekeeper.admin import IMessage, AdminRoot, MessagesRoot
from gatekeeper.app import GateKeeper
from uvclight import name, context, get_template, Page
from zope.interface import Interface
from dolmen.view import make_layout_response


class Timeout(Page):
    context(Interface)
    template = get_template('timeout.pt', __file__)


class Unauthorized(Page):
    context(Interface)
    template = get_template('unauthorized.pt', __file__)
    message = None

    def set_message(self, message):
        self.message = message


class NotFound(Page):
    context(Interface)
    template = get_template('404.pt', __file__)


class GatekeeperIndex(Page):
    name('index')
    context(GateKeeper)
    template = get_template('entrance.pt', __file__)

    def update(self):
        self.portals = list(self.context.get_portals(self.request))


class AdminIndex(Page):
    name('index')
    context(AdminRoot)
    template = get_template('admin.pt', __file__)

    def update(self):
        self.links = ({
            'title': u"Messages management",
            'url': get_absolute_url(self.context.messages, self.request),
            },)


class DeleteEntry(Action):

    def __call__(self, form):
        form.updateLines(mark_selected=True)
        session = get_session(form.context.db_key)
        for line in form.lines:
            if line.selected:
                obj = line.getContent()
                session.delete(obj)
        send(u"Deletion successful.")
        url = get_absolute_url(form.context, form.request)
        return SuccessMarker('Deleted', True, url=url)
        

class MessagesIndex(TableForm):
    name('index')
    context(MessagesRoot)

    ignoreRequest = False
    ignoreContent = False
    postOnly = True
    responseFactory = Response
    make_response = make_layout_response
    mode = DISPLAY

    actions = Actions(DeleteEntry('Delete'))

    @property
    def tableFields(self):
        fields = Fields(IMessage)
        fields['id'].mode = 'link'
        return fields

    def getItems(self):
        return list(self.context)

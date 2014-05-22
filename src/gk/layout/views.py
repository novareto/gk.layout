# -*- coding: utf-8 -*-

from cromlech.webob import Response
from cromlech.sqlalchemy import get_session
from dolmen.forms.base import DISPLAY, SuccessMarker
from dolmen.forms.base import Actions, Action
from dolmen.location import get_absolute_url
from dolmen.message.utils import send
from gatekeeper.admin import IMessage, AdminRoot, MessagesRoot
from gatekeeper.app import GateKeeper
from uvclight import name, context, get_template
from uvclight import AddForm, Page, Fields, TableForm
from zope.interface import Interface
from . import i18n as _


class Timeout(Page):
    template = get_template('timeout.pt', __file__)


class Unauthorized(Page):
    template = get_template('unauthorized.pt', __file__)
    message = None

    def set_message(self, message):
        self.message = message


class NotFound(Page):
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
        send(_(u"Deletion successful."))
        url = get_absolute_url(form.context, form.request)
        return SuccessMarker('Deleted', True, url=url)


class MessagesIndex(TableForm):
    name('index')
    context(MessagesRoot)

    ignoreRequest = False
    ignoreContent = False
    postOnly = True
    mode = DISPLAY
    css_class = "table table-striped table-condensed"

    actions = Actions(DeleteEntry(_('Delete')))

    @property
    def tableFields(self):
        fields = Fields(IMessage)
        fields['id'].mode = 'link'
        return fields

    def getItems(self):
        return list(self.context)

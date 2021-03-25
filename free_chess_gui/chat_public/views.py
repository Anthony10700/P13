from django.views import generic
from braces.views import LoginRequiredMixin
from . import models
from . import utils
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render


class DialogListView(LoginRequiredMixin, generic.ListView):
    template_name = 'chat_public/dialogs.html'
    model = models.Dialog
    ordering = 'modified'
    login_url = '/chat_public/connect_required.html'
    redirect_field_name = ""

    def get_queryset(self):
        dialogs = models.Dialog.objects.filter(
            Q(owner=self.request.user) | Q(opponent=self.request.user))
        return dialogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs.get('username'):
            user = get_object_or_404(
                get_user_model(),
                username=self.kwargs.get('username'))
            if user.username == "chat_user_all":
                if len(utils.get_dialogs_with_user(
                        self.request.user, user)) == 0:
                    dialog = models.Dialog.objects.create(
                        owner=self.request.user,
                        opponent=user)

                dial_to_send = []
                messages = models.Message.objects.all().order_by('-id')[:20]
                messages = list(reversed(messages))
                for messa in messages:
                    if str(messa.dialog.opponent) == "chat_user_all":
                        dial_to_send.append(messa)
                dialog = dial_to_send
            else:
                dialog = utils.get_dialogs_with_user(self.request.user, user)

            if len(dialog) == 0:
                dialog = models.Dialog.objects.create(
                    owner=self.request.user, opponent=user)
                context['active_dialog'] = dialog
            else:
                if user.username == "chat_user_all":
                    dialog = dialog
                    context['active_dialog'] = dialog
                else:
                    dialog = dialog[0]
                    context['active_dialog'] = [dialog]
        else:
            context['active_dialog'] = self.object_list[0]
        context['opponent_username'] = user
        context['ws_server_path'] = '{}://{}:{}/'.format(
            settings.CHAT_WS_SERVER_PROTOCOL,
            settings.CHAT_WS_SERVER_HOST,
            settings.CHAT_WS_SERVER_PORT,
        )
        return context


def connect_required(request):
    """
    connect_required

    Args:
        request ([type]): [description]
    """
    return render(request, 'chat_public/connect_required.html',  context={})

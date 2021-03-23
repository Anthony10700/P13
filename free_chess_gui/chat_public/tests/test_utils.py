from test_plus.test import TestCase
from chat_public.utils import get_dialogs_with_user, get_user_from_session
from django.contrib.sessions.models import Session
from chat_public.models import Dialog, Message


class TestUtilsFunctions(TestCase):
    def setUp(self):
        self.user1 = self.make_user(username="user1")
        self.user2 = self.make_user(username="user2")

    def test_get_dialogs_with_user(self):
        self.dialog = Dialog()
        self.dialog.owner = self.user2
        self.dialog.opponent = self.user1
        self.dialog.save()
        dialog = get_dialogs_with_user(self.user1, self.user2)[0]
        self.assertEqual(dialog, self.dialog)

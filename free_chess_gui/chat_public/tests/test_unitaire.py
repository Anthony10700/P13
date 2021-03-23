"""
        class of test Services chat_public
    """
import json
from django.test import RequestFactory, TransactionTestCase, Client
from django.contrib.auth import logout, get_user_model


# Create your tests here.


class TestServicesChat_publicUnitaire(TransactionTestCase):
    """class of test Services chat_public Unitaire API

    Args:
        TransactionTestCase ([type]): TransactionTestCase and not
        TestCase because Every test needs "setUp method"
    """
    reset_sequences = True

    def setUp(self):
        """[summary]
        """

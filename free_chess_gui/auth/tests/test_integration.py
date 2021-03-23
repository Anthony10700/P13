"""
        class of test Services Auth
    """
from django.test import RequestFactory, TransactionTestCase, Client, TestCase
from django.contrib.auth import logout, get_user_model
from auth.services.auth_services import sign_validation, account_get_info,\
    connect_validation


class TestServicesAuthIntegration(TransactionTestCase):
    """class of test Services Auth integration

    Args:
        TransactionTestCase ([type]): TransactionTestCase and not
        TestCase because Every test needs "setUp method"
    """
    reset_sequences = True

    def setUp(self):
        """[summary]
        """
        # Every test needs a client.
        self.factory = RequestFactory()
        self.client = Client()

    def make_account(self):
        """this method can create an account for the test
        """
        info = {
            "inputUsername": "Test_accound2",
            "inputemail": "Test-accound@monmail.com2",
            "inputPassword1": "Test_psw2",
            "inputPassword2": "Test_psw2",
            "inputNom": "Test_Nom",
            "inputprenom": "Test_prenom"}
        response = self.client.post('/auth/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])

    def test_sign_validation(self):
        """this method test the inscription
        """
        info = {
            "inputUsername": "Test_accound",
            "inputemail": "Test-accound@monmail.com",
            "inputPassword1": "Test_psw",
            "inputPassword2": "Test_psw",
            "inputNom": "Test_Nom",
            "inputprenom": "Test_prenom"}
        request = self.factory.post('/auth/sign_in.html', data=info)
        request.session = self.client.session
        result = sign_validation(request)
        result_dict = {
            "methode": "redirect",
            "value": "account",
            "user_is_connect": True}
        self.assertEqual(result, result_dict)

    def test_account_get_info(self):
        """this method test the account information
        """
        user = get_user_model()
        request = self.factory.get('/auth/account.html')
        request.user = user.objects.create_user(
            username='jacob', email='jacob@test.fr', password='top_secret')
        account_get = account_get_info(request)
        request.session = self.client.session
        request_response_dict = {
            "title": "Bienvenue " + request.user.username,
            "account_info": {"Email": request.user.email,
                             "Speudo": request.user.username,
                             "Prénom": request.user.first_name,
                             "Nom": request.user.last_name}}
        self.assertEqual(account_get, request_response_dict)
        logout(request)
        account_get = account_get_info(request)
        request_response_dict = {}
        self.assertEqual(account_get, request_response_dict)

    def test_connect_validation(self):
        """this method test the account connection
        """
        self.make_account()
        info = {
            "inputEmail_connect": "Test-accound@monmail.com2",
            "inputPassword_connect": "Test_psw2"}
        request = self.factory.post('/auth/connect', data=info)
        request.session = self.client.session
        # request.user = User.objects.get(username="Test_accound2")
        result_dict = {
            "methode": "redirect",
            "value": "account",
            "user_is_connect": True}
        resulta = connect_validation(request)
        self.assertEqual(result_dict, resulta)


class TestUrlAuth(TestCase):
    """
    Class test of url of app auth (test views)

    Args:
        TestCase ([type]): [description]
    """

    def setUp(self):
        """This method similar at __init__ for each instance
        """
        # Every test needs a client.
        self.client = Client()

    def test_sign_in(self):
        """
        This method test the sign_in url
        """
        response = self.client.get('/auth/sign_in.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Inscription")

        self.make_account()

        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/sign_in.html')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/account.html")

    def test_accound(self):
        """This methode test the account url
        """
        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 302)

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"],
            "Test-accound@monmail.com")

    def test_deconnection(self):
        """This method test the deconnection url
        """
        response = self.client.get('/auth/deconnection')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['title'], "Vous n'êtes pas connecté.")

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/deconnection')
        self.assertEqual(response.context['title'], "Déconnexion")

    def test_connect(self):
        """This method test the connection url
        """
        response = self.client.get('/auth/connect')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Account")

        self.make_account()

        info = {"inputEmail_connect": "Test-accound@monmail.com",
                "inputPassword_connect": "Test_psw"}
        response = self.client.post('/auth/connect', data=info)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/account.html")

        info = {"inputEmail_connect": "Test-accound@monmail.com",
                "inputPassword_connect": "Tsdqsdqs"}
        response = self.client.post('/auth/connect', data=info)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/sign_in.html")

    def make_account(self):
        """This method make a account for testing the url form sign_in
        """
        info = {"inputUsername": "Test_accound",
                "inputemail": "Test-accound@monmail.com",
                "inputPassword1": "Test_psw",
                "inputPassword2": "Test_psw",
                "inputNom": "Test_Nom",
                "inputprenom": "Test_prenom"}
        response = self.client.post('/auth/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])

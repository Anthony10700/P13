"""this file is for including the job code

    Returns:
        [type]: [description]
    """
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from auth.forms import CustomUserCreationForm


def sign_validation(request):
    """This method test if a form is valide return to a dictionary

    Args:
       request (request): views request

    Returns:
        dictionary: "methode": "", "value": ""
    """
    result_dict = {"methode": "", "value": ""}
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.clean_password2()
        form.clean_email()
        form.clean_pseudo()
        user = form.save()
        login(request, user)
        result_dict["methode"] = "redirect"
        result_dict["value"] = "account"
        result_dict["user_is_connect"] = True
        return result_dict
    else:
        result_dict["user_is_connect"] = False
        result_dict["methode"] = "render"
        result_dict["value"] = "auth/sign_in.html"
        result_dict["form"] = form
        return result_dict


def connect_validation(request):
    """
    This method test if connection is valid

    Args:
        request (request): views request

    Returns:
        dictionary: "methode": "", "value": "" ,"messages":""
    """
    result_dict = {"methode": "", "value": ""}
    if 'inputPassword_connect' in request.POST \
            and 'inputEmail_connect' in request.POST:
        email = request.POST['inputEmail_connect']
        password = request.POST['inputPassword_connect']
        password = make_password(password=password,
                                 salt="1",
                                 hasher='pbkdf2_sha256')
        user_get = get_user_model()
        try:
            user_tmp = user_get.objects.get(email=email)
        except user_get.DoesNotExist:
            user_tmp = None
        if user_tmp is not None:
            user = authenticate(request,
                                username=user_tmp.username, password=password)
        else:
            user = None
        if user is not None:
            login(request, user)
            request.session.set_expiry(3600)
            request.session.clear_expired()
            result_dict["methode"] = "redirect"
            result_dict["value"] = "account"
            result_dict["user_is_connect"] = True
            return result_dict
        else:
            result_dict["user_is_connect"] = False
            result_dict["methode"] = "redirect"
            result_dict["value"] = "sign_in"
            result_dict["messages"] = "Mot de passe ou pseudo incorrect"
            return result_dict
    else:
        result_dict["user_is_connect"] = False
        result_dict["methode"] = "render"
        result_dict["value"] = "auth/sign_in.html"
        return result_dict


def account_get_info(request):
    """This method create a context of user information  if he is connected

    Args:
        request (request): request of views auth account

    Returns:
        dict: context of render accound info
    """
    if request.user.is_authenticated:

        user = request.user
        context = {"title": "Bienvenue " + user.username,
                            "account_info": {"Email": user.email,
                                             "Speudo": user.username,
                                             "Prénom": user.first_name,
                                             "Nom": user.last_name}}
        return context
    return {}
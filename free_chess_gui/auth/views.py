from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from auth.services.auth_services import connect_validation, account_get_info,\
    sign_validation
# Create your views here.


def sign_in(request):
    """this view concern the inscription

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """

    if not request.user.is_authenticated:
        if request.method == 'POST':
            try:
                result_dict = sign_validation(request)
                if result_dict["methode"] == "redirect":
                    return redirect(result_dict["value"])
                elif result_dict["methode"] == "render":
                    context = {'form': result_dict["form"],
                               "user_is_connect": False}
                    return render(request, result_dict["value"],
                                  context=context)
            except ValidationError as err:
                messages.error(request, err.message)
                return redirect('sign_in')

        else:
            context = {'title': "Inscription",
                       "user_is_connect": False}
            return render(request, 'auth/sign_in.html',  context=context)
    else:
        return redirect('account')


def connect(request):
    """this view concern the account connection

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        result_dict = connect_validation(request)
        if result_dict["methode"] == "redirect":
            if result_dict["value"] == "account":
                return redirect(result_dict["value"])
            elif result_dict["value"] == "sign_in":
                messages.error(request, result_dict["messages"])
                return redirect(result_dict["value"])
        if result_dict["methode"] == "render":
            context = {'title': "Account",
                       "user_is_connect": False}
            return render(request, result_dict["value"],  context=context)
    else:
        context = {'title': "Account",
                   "user_is_connect": False}
        return render(request, 'auth/sign_in.html',  context=context)


def account(request):
    """this view concern the account

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        context = account_get_info(request)
        context["title"] = "Account"
        context["user_is_connect"] = True
        return render(request, 'auth/account.html', context=context)
    else:
        return redirect("index")


def logout_view(request):
    """this view is for the deconnexion

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        logout(request)
        context = {'title': "Déconnexion",
                   "user_is_connect": False}
        return redirect("index")
    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté.",
                   "user_is_connect": False}
        return render(request, 'auth/sign_in.html',  context=context)
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, render
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


# Create your views here.
def home(request: HttpRequest):
    return render(request, "index.html")


def google_login(request):
    code = request.GET.get("code")
    print("{0}://{1}{2}".format(request.scheme, request.get_host(), request.path))
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ],
        redirect_uri="{0}://{1}{2}".format(
            request.scheme, request.get_host(), request.path
        ),
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    if code is None:
        return redirect(authorization_url)
    flow.fetch_token(code=code)
    credentials = flow.credentials

    user_info_service = build("oauth2", "v2", credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    request.session["user_info"] = user_info

    return redirect("home")


def logout_session(request):
    request.session["user_info"] = None
    return redirect("home")

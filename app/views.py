from django.http import HttpRequest
from django.shortcuts import redirect, render
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


# Create your views here.
def home(request: HttpRequest):
    stored_credentials = request.session.get("credentials", None)
    if stored_credentials is not None:
        user_info_service = build(
            "oauth2",
            "v2",
            credentials=Credentials(**request.session.get("credentials")),
        )
        user_info = user_info_service.userinfo().get().execute()
        return render(
            request, "index.html", {"user_info": user_info, "is_authenticated": True}
        )
    return render(request, "index.html", {"is_authenticated": False})


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

    request.session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "granted_scopes": credentials.granted_scopes,
    }

    return redirect("home")


def logout_session(request):
    request.session["credentials"] = None
    return redirect("home")

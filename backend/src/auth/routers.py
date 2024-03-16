import urllib.parse
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from starlette.responses import Response

from src.core.config import KeyCloakSettings
from .core import idp, get_current_user

router = APIRouter(prefix="", tags=["auth"])


@router.get("/user")
def current_user(access_token: Annotated[str | None, Cookie()] = None):
    user = get_current_user(access_token)
    if user is None:
        return Response(status_code=401)
    return user


@router.get("/login")
def login_redirect():
    # Note: add 'openid' to scope if you want to read `/userinfo`
    return RedirectResponse(idp.login_uri)


@router.get("/logout")
def logout_redirect():
    return RedirectResponse(
        idp.logout_uri
        + "?post_logout_redirect_uri="
        + urllib.parse.quote_plus(KeyCloakSettings.logout_callback_uri)
        + "&client_id="
        + KeyCloakSettings.client_id
    )


@router.get("/login/callback")
def callback(session_state: str, code: str):
    authorization_code = idp.exchange_authorization_code(
        session_state=session_state, code=code
    )
    token = authorization_code.access_token
    response = RedirectResponse(url=KeyCloakSettings.login_callback_uri)
    response.set_cookie(
        "access_token",
        value=token,
        httponly=True,
        secure=True,
        domain=KeyCloakSettings.domain,
        samesite="none",
    )
    return response


@router.get("/logout/callback")
def logout_callback():
    response = RedirectResponse(url=KeyCloakSettings.logout_callback_uri)
    response.delete_cookie(
        "access_token",
        httponly=True,
        secure=True,
        domain=KeyCloakSettings.domain,
        samesite="none",
    )
    return response

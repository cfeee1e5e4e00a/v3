import urllib.parse
from typing import Annotated, List

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_keycloak import FastAPIKeycloak
from keycloak import KeycloakOpenID
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from starlette.responses import Response

from conf import (DOMAIN, KC_URL, KC_REALM,
                      KC_CLIENT_ID, KC_CLIENT_SECRET,
                      KC_LOGIN_CALLBACK_URI, KC_LOGOUT_CALLBACK_URI)
from conf import LOGIN_CALLBACK_URI, LOGOUT_CALLBACK_URI

router = APIRouter(
    prefix="",
    tags=["auth"]
)


class SimpleFastAPIKeycloak(FastAPIKeycloak):
    def _get_admin_token(self) -> None:
        return None


class KcUser(BaseModel):
    id: str
    name: str
    roles: List[str]


idp = SimpleFastAPIKeycloak(
    server_url=KC_URL,
    client_id=KC_CLIENT_ID,
    client_secret=KC_CLIENT_SECRET,
    admin_client_secret="",
    realm=KC_REALM,
    callback_uri=KC_LOGIN_CALLBACK_URI
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=idp.token_uri)

keycloak_openid = KeycloakOpenID(server_url=KC_URL,
                                 realm_name=KC_REALM,
                                 client_id=KC_CLIENT_ID,
                                 client_secret_key=KC_CLIENT_SECRET)
KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"


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
    return RedirectResponse(idp.logout_uri + "?post_logout_redirect_uri=" +
                            urllib.parse.quote_plus(KC_LOGOUT_CALLBACK_URI) +
                            "&client_id=" + KC_CLIENT_ID)


@router.get("/login/callback")
def callback(session_state: str, code: str):
    authorization_code = idp.exchange_authorization_code(session_state=session_state, code=code)
    token = authorization_code.access_token
    response = RedirectResponse(url=LOGIN_CALLBACK_URI)
    response.set_cookie("access_token", value=token,
                        httponly=True, secure=True,
                        domain=DOMAIN,
                        samesite="none")
    return response


@router.get("/logout/callback")
def logout_callback():
    response = RedirectResponse(url=LOGOUT_CALLBACK_URI)
    response.delete_cookie("access_token",
                           httponly=True, secure=True,
                           domain=DOMAIN,
                           samesite="none")
    return response


def get_current_user(access_token: str):
    if not access_token:
        return None
    options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
    token = keycloak_openid.decode_token(access_token, key=KEYCLOAK_PUBLIC_KEY, options=options)
    return KcUser(id=token.get("sub"), name=token.get("preferred_username"),
                  roles=token.get("realm_access").get("roles"))


async def secretary_auth_guard(token: Annotated[str, Depends(oauth2_scheme)]):
    user = get_current_user(token)
    _check_role(user, 'secretary')
    return user


def _check_role(user: KcUser, role: str):
    if user is None or role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Only '{role}' role is allowed",
            headers={"WWW-Authenticate": "Bearer"}
        )

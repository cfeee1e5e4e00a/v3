from typing import Annotated
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer
from fastapi_keycloak import FastAPIKeycloak
from fastapi import Depends, HTTPException, status
from keycloak import KeycloakOpenID

from src.core.config import KeyCloakSettings


class SimpleFastAPIKeycloak(FastAPIKeycloak):
    def _get_admin_token(self) -> None:
        return None


class KcUser(BaseModel):
    id: str
    name: str
    roles: list[str]


idp = SimpleFastAPIKeycloak(
    server_url=KeyCloakSettings.url,
    client_id=KeyCloakSettings.client_id,
    client_secret=KeyCloakSettings.client_secret,
    admin_client_secret="",
    realm=KeyCloakSettings.realm,
    callback_uri=KeyCloakSettings.login_callback_uri,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=idp.token_uri)

keycloak_openid = KeycloakOpenID(
    server_url=KeyCloakSettings.url,
    realm_name=KeyCloakSettings.realm,
    client_id=KeyCloakSettings.client_id,
    client_secret_key=KeyCloakSettings.client_secret,
)
KEYCLOAK_PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n"
    + keycloak_openid.public_key()
    + "\n-----END PUBLIC KEY-----"
)


def get_current_user(access_token: str):
    if not access_token:
        return None
    options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
    token: dict = keycloak_openid.decode_token(
        access_token, key=KEYCLOAK_PUBLIC_KEY, options=options
    )
    return KcUser(
        id=token.get("sub"),
        name=token.get("preferred_username"),
        roles=token.get("realm_access").get("roles"),
    )


async def secretary_auth_guard(token: Annotated[str, Depends(oauth2_scheme)]):
    user = get_current_user(token)
    _check_role(user, "secretary")
    return user


def _check_role(user: KcUser, role: str):
    if user is None or role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Only '{role}' role is allowed",
            headers={"WWW-Authenticate": "Bearer"},
        )

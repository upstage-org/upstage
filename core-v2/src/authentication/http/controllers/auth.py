from fastapi import APIRouter, Depends, Request
from authentication.http.dtos.login import LoginDTO
from authentication.services.auth import AuthenticationService
from bootstraps import app
from core.decorators.current_user import get_current_user
from users.entities.user import UserEntity

router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post("/access_token")
async def login(
    request: Request,
    payload: LoginDTO,
    authentication_service: AuthenticationService = Depends(),
):
    return await authentication_service.login(payload, request)


@router.post("/refresh_token")
async def refresh_token(
    request: Request,
    current_user: UserEntity = Depends(get_current_user),
    authentication_service: AuthenticationService = Depends(),
):
    return await authentication_service.refresh_token(current_user, request)


@router.delete("/access_token")
async def logout(
    request: Request, authentication_service: AuthenticationService = Depends()
):
    return await authentication_service.logout(request)


app.include_router(router)

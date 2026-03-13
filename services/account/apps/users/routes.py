from django.shortcuts import get_object_or_404
from http import HTTPStatus
from .models import User
from .schemas import UserRead, UserCreate, UserUpdate
from ninja import Router
from ninja_jwt.authentication import JWTAuth

router = Router(tags=["Users"], auth=JWTAuth())


@router.post("/", response={HTTPStatus.CREATED: UserRead})
def user_create(request, payload: UserCreate):
    user = User.objects.create(**payload.dict())
    return user


@router.get("me/", response=UserRead)
def user_read(request):
    return request.user


@router.patch("me/", response=UserRead)
def user_update(request, user_id: int, payload: UserUpdate):
    user = get_object_or_404(User, pk=user_id)

    if user != request.user:
        return HTTPStatus.FORBIDDEN, {"detail": "Sem permissão"}
    
    update_data = payload.dict(exclude_unset=True)

    for attr, value in update_data.items():
        setattr(user, attr, value)

    user.save()

    return user


@router.delete("me/", response={HTTPStatus.NO_CONTENT: None})
def user_delete(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)

    if user != request.user:
        return HTTPStatus.FORBIDDEN, {"detail": "Sem permissão"}

    user.delete()

    return HTTPStatus.NO_CONTENT, None

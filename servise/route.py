from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from servise.model_request import Registration, ConfirmRegistration
from servise.views import authorization, confirm_registration_user
from database.connection import get_db


router = APIRouter(prefix='/registr')


@router.post('/registration')
async def post_authorization(register: Registration, db: Session = Depends(get_db)):
    rsult = await authorization(register, db)
    return rsult


@router.post('/confirmation-registration')
async def confirmation_registration(confirm_user: ConfirmRegistration, db: Session = Depends(get_db)):
    result = await confirm_registration_user(confirm_user, db)
    return result
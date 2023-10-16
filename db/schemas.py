from pydantic import BaseModel, EmailStr
from typing import Optional

class user(BaseModel):

    email:EmailStr
    country_code:str
    phone_number:str
    plan:Optional[str]="basic"
    is_superuser:Optional[bool]=False
    password:str

class login(BaseModel):
    phonenumber:str
    password:str

class url(BaseModel):
    photoaddress:str
from pydantic import BaseModel, Field, ConfigDict, EmailStr, UUID4


class RegisterUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    email: EmailStr = Field(..., description="Email address")


class LoginUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")


class GetTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: float = Field(..., description="Amount")
    bill_id: UUID4 = Field(..., description="Bill ID")


class GetUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email address")


class GetBill(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    balance: float = Field(..., description="Balance")
    uuid: UUID4 = Field(..., alias="id", description="UUID4")
    user: GetUser = Field(..., description="User")
    bill_transactions: list[GetTransaction] = Field(..., description="Transaction")

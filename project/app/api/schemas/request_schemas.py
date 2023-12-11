from pydantic import BaseModel, Field


class Patient(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z ]+$", default="Nombre Falso")
    email: str = Field(
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        default="email@falso.com",
    )
    address: str = "Address"
    phone: str = Field(
        pattern=r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", default="1111111111"
    )

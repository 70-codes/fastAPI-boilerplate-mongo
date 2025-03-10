from pydantic import BaseModel


class UserShow(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    id: str
    f_name: str
    l_name: str
    password: str
    username: str
    email: str
    phone: str

    class config:
        orm_mode = True

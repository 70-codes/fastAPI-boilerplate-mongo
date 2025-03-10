from pydantic import BaseModel


class User(BaseModel):
    """
    User model for creating a user in the system.
    Used in the request body.

    Attributes:
        f_name (str): The first name of the user.
        l_name (str): The last name of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        phone (str): The phone number of the user.
    """

    f_name: str
    l_name: str
    username: str
    email: str
    password: str
    phone: str

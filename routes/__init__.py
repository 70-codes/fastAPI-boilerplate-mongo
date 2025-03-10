from fastapi import APIRouter


def create_router(prefix, tags):
    """_summary_

    Args:
        prefix (_type_): _description_
        tags (_type_): _description_

    Returns:
        _type_: _description_
    """
    return APIRouter(
        prefix=f"/{prefix}",
        tags=[f"{tags}"],
    )

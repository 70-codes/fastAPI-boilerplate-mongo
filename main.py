#!/home/creed347/anaconda3/envs/fastAPI/bin/python


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth import auth
from routes.user import user

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"message": "Hello World"}


app.include_router(user)
app.include_router(auth)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

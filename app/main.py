from fastapi import FastAPI, HTTPException
import os
import uuid

app = FastAPI()


def is_ready() -> bool:

    get_author()
    get_id()

    return True


@app.get("/hostname")
def get_hostname():
    return {"hostname": os.uname().nodename}


@app.get("/author")
def get_author():
    author = os.getenv("AUTHOR")
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"author": author}


@app.get("/id")
def get_id():
    uuid_value = os.getenv("UUID")

    if not uuid_value:
        raise HTTPException(status_code=404, detail="UUID not found")

    try:
        uuid.UUID(uuid_value, version=4)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="UUID is not in correct format")

    return {"uuid": uuid_value}


@app.get("/readiness")
def get_readiness():
    is_ready()
    return {"status": "Ready"}


@app.get("/liveness")
def liveness():
    return {"status": "Alive"}

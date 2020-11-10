from fastapi import FastAPI, HTTPException
from main import go_parse as go_parse_

app = FastAPI()


@app.post("/go_parse")
def go_parse(string: str):
    try:
        result = go_parse_(string)
    except Exception as err:
        raise HTTPException(status_code=500, detail=ascii(err))

    return result

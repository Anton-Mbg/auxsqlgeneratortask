from fastapi import FastAPI, HTTPException

app = FastAPI()

SCHEMA_V2 = {
    "fields": [
        {
            "name": "auxUserId",
            "type": "int"
        },
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "birthday",
            "type": {
                "logicalType": "date",
                "type": "int"
            }
        },
        {
            "name": "createdAt",
            "type": "string"
        }
    ],
    "name": "user_created",
    "type": "record"
}


SCHEMA_V1 = {
    "fields": [
        {
            "name": "auxUserId",
            "type": "int"
        },
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "birthday",
            "type": "string",
        },
        {
            "name": "createdAt",
            "type": "string"
        }
    ],
    "name": "user_created",
    "type": "record"
}


# TODO schema of the response
@app.get("/schema/{version_id}")
def schema(version_id: int) -> dict:
    match version_id:
        case 1:
            return SCHEMA_V1
        case 2:
            return SCHEMA_V2
        case _:
            raise HTTPException(404, detail="unknown version")

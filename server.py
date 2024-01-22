from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class AvroLogicalType(BaseModel):
    logicalType: str
    type: str


class AvroSchemaFields(BaseModel):
    name: str
    type: str | AvroLogicalType


class AvroSchema(BaseModel):
    name: str
    type: str
    fields: list[AvroSchemaFields]


SCHEMAS = {
    "user_created": {
        1: AvroSchema(
            name="user_created",
            type="record",
            fields=[
                AvroSchemaFields(name="auxUserId", type="int"),
                AvroSchemaFields(name="name", type="string"),
                AvroSchemaFields(name="birthday", type="string"),
                AvroSchemaFields(name="createdAt", type="string"),
            ],
        ),
        2: AvroSchema(
            name="user_created",
            type="record",
            fields=[
                AvroSchemaFields(name="auxUserId", type="int"),
                AvroSchemaFields(name="name", type="string"),
                AvroSchemaFields(
                    name="birthday", type=AvroLogicalType(logicalType="date", type="int")
                ),
                AvroSchemaFields(name="createdAt", type="string"),
            ],
        ),
    }
}


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    """Redirects to the docs."""
    raise HTTPException(307, headers={"Location": "/docs"})


@app.get(
    "/schema",
    response_model=tuple[str, ...],
    response_description="List of available schemas.",
)
def get_schemas():
    """Returns all available schemas."""
    return tuple(SCHEMAS.keys())


@app.get(
    "/schema/{schema_name}",
    response_model=tuple[int, ...],
    response_description="List of available versions for this schema.",
)
def get_schema_versions(schema_name: str):
    """Returns all available version numbers for this schema."""
    try:
        schema = SCHEMAS[schema_name]
    except KeyError:
        raise HTTPException(404, detail="unknown schema")
    return tuple(schema.keys())


@app.get(
    "/schema/{schema_name}/{version_id}",
    response_model=AvroSchema,
    response_description="The schema for the given version.",
)
def get_schema(schema_name: str, version_id: int):
    """Returns the schema for the given version."""
    try:
        schema = SCHEMAS[schema_name]
    except KeyError:
        raise HTTPException(404, detail="unknown schema")

    try:
        return schema[version_id]
    except KeyError:
        raise HTTPException(404, detail="unknown version")

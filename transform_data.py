import asyncio
import json

import fastavro
import httpx
import psycopg

import init_db


async def requestLatestSchemaVersion():
    url = "http://0.0.0.0:8000/schema/user_created"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        versions = response.read().decode('utf-8')
        versions_decoded = json.loads(versions)
        latest_version = versions_decoded[-1]

    return latest_version


async def requestLatestSchema(version):
    url = "http://0.0.0.0:8000/schema/user_created/" + str(version)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        schema = response.read().decode('utf-8')
        schema_decoded = json.loads(schema)

        fields = schema_decoded['fields']


    return fields



def create_transformed_data_table():
    data_rows = requestRawData()
    with psycopg.connect(
            "host=localhost dbname=postgres user=postgres password=postgres"
    ) as conn:
        conn.execute("DROP TABLE IF EXISTS transformed_data;")

        conn.execute("CREATE TABLE transformed_data ("
                     "id serial, "
                     "aux_user_id int , "
                     "name varchar, "
                     "birthday date, "
                     "created_at timestamp)")

        for row in data_rows:

            aux_id = row['aux_user_id']
            name = row['name']
            birthday_as_date = init_db.days_from_unix_epoch_to_date(row['birthday'])
            created_at_utc = init_db.timestamp_to_utc_timestamp(row['created_at'])
            conn.execute("INSERT INTO transformed_data (aux_user_id, name, birthday, created_at) VALUES (%s,%s,%s,%s);",(aux_id,name,birthday_as_date,created_at_utc))


def requestRawData():

    with psycopg.connect(
            "host=localhost dbname=postgres user=postgres password=postgres"
    ) as conn:

        cursor = conn.cursor()
        table_name = "raw_data"
        column_name = "data"

        query = f"SELECT {column_name} FROM {table_name};"
        cursor.execute(query)

        results = [tup[0] for tup in cursor.fetchall()]

       

        return results


schema_Version = asyncio.run(requestLatestSchemaVersion())
avro_schema = asyncio.run(requestLatestSchema(schema_Version))
schema = server.
# Die Data Column muss hier noch entsprechend dem Avro-Schema geparsed werden


create_transformed_data_table()

#%%

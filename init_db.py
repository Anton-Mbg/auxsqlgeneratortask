
import json
import random
from datetime import date, datetime, timedelta, timezone

import psycopg
import pytz
from faker import Faker


def datetime_to_europe_berlin_string(dt: datetime) -> str:
    return dt.astimezone(tz=pytz.timezone("Europe/Berlin")).isoformat()

def date_to_days_from_unix_epoch(tstamp: date) -> int:
    return (tstamp - date(1970, 1, 1)).days

def days_from_unix_epoch_to_date(days: int) -> date:
    epoch_date = datetime(1970, 1, 1)
    birthday_date = epoch_date + timedelta(days=days)

    return birthday_date

def timestamp_to_utc_timestamp(timestamp: str) -> datetime:

    input_timestamp = datetime.fromisoformat(timestamp)

    utc_timestamp = input_timestamp.astimezone(tz=timezone.utc)
    return utc_timestamp

def get_fake_data(count: int = 10) -> list[dict]:
    fake = Faker()

    return [
        {
            "aux_user_id": random.randint(1_000_000, 10_000_000),
            "name": fake.name(),
            # das generiert nur Daten für Schema 2. Ist das gewollt?
            "birthday": date_to_days_from_unix_epoch(fake.date_of_birth(minimum_age=18, maximum_age=80)),
            "created_at": datetime_to_europe_berlin_string(fake.date_time_this_decade()),
        }
        for _ in range(count)
    ]


def init_db():
    with psycopg.connect(
        "host=localhost dbname=postgres user=postgres password=postgres"
    ) as conn:
        conn.execute("DROP TABLE IF EXISTS raw_data;")
        conn.execute("CREATE TABLE raw_data (id serial, data json);")
        for entry in get_fake_data(count=1000):
            conn.execute(
                "INSERT INTO raw_data (data) VALUES (%s);", (json.dumps(entry),)
            )


if __name__ == "__main__":
   init_db()

#%%

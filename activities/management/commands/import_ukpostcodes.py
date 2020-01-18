# Run reset.sh to rebuild the database if you also need that done.
from django.core.management.base import BaseCommand
from django.db import connection
import os, sys, subprocess



presql =[
"drop table if exists postcodelatlng",
"drop table if exists distcitlatlng",
"pragma JOURNAL_MODE=OFF",
"pragma SYNCHRONOUS=OFF",
"pragma LOCKING_MODE=EXCLUSIVE",
"pragma TEMP_STORE=MEMORY",
"""
CREATE TABLE IF NOT EXISTS postcodelatlng (
id INTEGER PRIMARY KEY,
postcode CHARACTER(10),
latitude DECIMAL(19,15),
longitude DECIMAL(19,15)
)""",
"""CREATE TABLE IF NOT EXISTS distcitlatlng (
id INTEGER PRIMARY KEY,
name VARCHAR(255),
area varchar(255),
postcode CHARACTER(10),
latitude DECIMAL(19,15),
longitude DECIMAL(19,15)
)"""
]

postsql = [
"CREATE INDEX IF NOT EXISTS post_code_index  ON postcodelatlng(postcode)",
"CREATE INDEX IF NOT EXISTS district_index  ON distcitlatlng(postcode)"
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            wd = os.getcwd()
            postcodesqls = wd + '/data/ukpostcodesmysql.sql'
            districtsls = wd + '/data/ukdistrictsmysql.sql'

            # Recreate our conversion table and index
            print("Dropping table and creating new")
            for sql in presql:
                cursor.execute(sql)
                print(sql)


            # Load raw data file which is already SQL, so we need to run it in
            print("Now importing SQL with all districts")
            with open(districtsls) as fp:
                for cnt, sql in enumerate(fp):
                    cursor.execute(sql)

            # Load raw data file which is already SQL, so we need to run it in
            print("Now importing SQL with all postcodes")
            with open(postcodesqls) as fp:
                for cnt, sql in enumerate(fp):
                    cursor.execute(sql)


            print("Creating indexes now")

            # Recreate our conversion table and index
            for sql in postsql:
                cursor.execute(sql)
                print(sql)

            print("Post code imported and done")
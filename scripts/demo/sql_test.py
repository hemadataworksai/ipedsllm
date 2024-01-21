#!/usr/bin/env python3

## This is a short snippet demonstrating how to send SQL queries using python. It retrieves 100 rows from the table OM2022 into a Pandas dataframe.
## To run this script, put a USER and PASSWORD with the appropriate permissions into the connection string.
## DO NOT commit this script back to the git repo with the USER and PASSWORD in it. It will expose our database to anybody who has access to this repo, which is everybody since our repo is public.

import pandas as pd
import psycopg2 as pg

engine = pg.connect("dbname='defaultdb' user='USER' host='db-postgresql-nyc3-10726-do-user-15531455-0.c.db.ondigitalocean.com' port='25060' password='PASSWORD'")
df = pd.read_sql('select * from "OM2022" limit 100', con=engine)

print(df)

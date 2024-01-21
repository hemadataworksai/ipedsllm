#!/usr/bin/env python3

import os,sys
import pandas as pd
from sqlalchemy import create_engine

file = sys.argv[1]
tablename = os.path.splitext(file)[0].upper()

df = pd.read_csv(file)
df.columns = [c.lower() for c in df.columns]
print(df)

## If you want to use this script, put in the USER and PASSWORD for a user with permissions before running it.
## DO NOT commit this script back to the git repo with the USER and PASSWORD in it. 
## It will expose the database to anyone who can view this repository, which is everybody since this repo is public.
engine = create_engine('postgresql://USER:PASSWORD@db-postgresql-nyc3-10726-do-user-15531455-0.c.db.ondigitalocean.com:25060/defaultdb')
df.to_sql(tablename, engine)

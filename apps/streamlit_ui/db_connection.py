import psycopg2
import os

def db_insert(data_to_insert):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB_NAME'),
            user=os.getenv('POSTGRES_DB_USERNAME'), 
            password=os.getenv('POSTGRES_DB_PASSWORD'), 
            host=os.getenv('POSTGRES_DB_HOST'), 
            port=os.getenv('POSTGRES_DB_PORT')
        )
        cur = conn.cursor()
    
        insert_query = f"""
                        INSERT INTO {os.getenv('POSTGRES_USR_TBL')} (email, username, password, date_joined)
                        VALUES (%s, %s, %s, %s)
                        """
        cur.execute(insert_query, data_to_insert)
    
        conn.commit()
        cur.close()
        conn.close()
    
    except Exception as e:
        print(f"An error occurred: {e}")



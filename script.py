import psycopg2
import time
from twilio.rest import Client

def connect_to_db():
    retry_attempts = 20
    for attempt in range(retry_attempts):
        # Connect to the database
        try:
            connection = psycopg2.connect(
                user="postgres.gfaxitbbwlclnuhqucqi",
                password="#542000Nd#",
                host="aws-0-eu-west-3.pooler.supabase.com",
                port="6543",
                dbname="postgres"
            )
            print("Connection successful!")
            
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()
            
            # Example query
            #cursor.execute("select * from exemplo1")

            cursor.execute("select id from exemplo1 ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            print(result[0])
            cursor.execute("Insert into exemplo1 (test) values (" + str(result[0]) + ");")
            connection.commit()
            cursor.execute("select * from exemplo1")
            result = cursor.fetchall() 
  
            # Printing all records or rows from the table. 
            # It returns a result set.  
            for all in result: 
                print(all)
        # result = cursor.fetchone()
        # print(result)

            # Close the cursor and connection
            cursor.close()
            connection.close()
            print("Connection closed.")
            account_sid = 'AC98012587e10cecccf2c8eff9b86243c1'
            auth_token = '408a38ccb7180467317ddca5ca41765f'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
              from_='whatsapp:+14155238886',
             # content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
              #content_variables='{"1":"12/1","2":"3pm"}',
              to='whatsapp:+351961065823',
              body = 'fodasse'
            )
            return
        except Exception as e:
            print(f"Failed to connect: {e}")
            time.sleep(1)
    return None

connection = connect_to_db()
if connection:
    print("Connected to the database")






import psycopg2
import datetime
from twilio.rest import Client
import requests
from urllib.parse import quote


def connect_to_db():
    retry_attempts = 1
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
            cursor = connection.cursor()
            
            cursor.execute("select last_time_alive, notification from wake_up_v2 ORDER BY id DESC")
            #print(cursor)
            result = cursor.fetchone()
          #  print(datetime.datetime.now())
            print(result)
            
            if(result is None):
                whatsapp("Atenção!! Falha de Eletricidade.")
                cursor.execute("insert into wake_up_v2(notification) values(1)")
                connection.commit()

            elif(time_calculate(result[0],datetime.datetime.now()) > 8 and result[1]==0):
                whatsapp("Atenção!! Falha de Eletricidade.")
                print("Correu mal")
                cursor.execute("update wake_up_v2 set notification = 1")
                connection.commit()
            elif(time_calculate(result[0],datetime.datetime.now()) > 8 and result[1]==1):    
                print("Continua mal")
            else:
                if(any_miss( cursor)):
                    # whatsapp("Eletricidade de volta!")
                    print("eletricidade de volta")
                print("Correu tudo bem")
                cursor.execute("delete from wake_up_v2")
                connection.commit()
                
                
            # Close the cursor and connection
            cursor.close()
            connection.close()
           # print("Connection closed.")
            
            return
        except Exception as e:
            print(f"Failed to connect: {e}")
    return None


def time_calculate(time1,time2):

    td = time2 - time1
   # print(td)
    td_mins = int(round(td.total_seconds() / 60))
    #print(td_mins)

    return td_mins


def any_miss(cursor):
    #print(cursor)
    for row in cursor:
        if(row[1] == 1):
            return 1
        #print(row)
    return 0
    
    
def whatsapp(message: str) -> str:
    print("""Send a Whatsapp message.""")

    text = quote(message)
    url = f'https://api.callmebot.com/whatsapp.php?phone=351917347946&text={text}&apikey=3163670'
    requests.post(url).text
    #url = f'https://api.callmebot.com/whatsapp.php?phone=351961065823&text={text}&apikey=9943501'
    print(url)
    return requests.post(url).text

connect_to_db()

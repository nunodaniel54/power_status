import psycopg2
import datetime
from twilio.rest import Client


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
            
            cursor.execute("select last_time_alive, notification from wake_up ORDER BY id DESC")
            #print(cursor)
            result = cursor.fetchone()
          #  print(datetime.datetime.now())
            print(result)
            
            if(result is None):
                send_msg("Atenção!! Falha de Eletricidade.")
                cursor.execute("insert into wake_up(notification) values(1)")
                connection.commit()

            elif(time_calculate(result[0],datetime.datetime.now()) > 5 and result[1]==0):
                send_msg("Atenção!! Falha de Eletricidade.")
                print("Correu mal")
                cursor.execute("update wake_up set notification = 1")
                connection.commit()
            elif(time_calculate(result[0],datetime.datetime.now()) > 5 and result[1]==1):    
                print("Continua mal")
            else:
                if(any_miss( cursor)):
                    send_msg("Eletricidade de volta!")
                    print("eletricidade de volta")
                print("Correu tudo bem")
                cursor.execute("delete from wake_up")
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

def send_msg(msg):
    account_sid = 'AC98012587e10cec' + 'ccf2c8eff9b86243c1'
    auth_token = '2941d9aa2cd4316d' + 'ae1cf274fa4be156'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    # content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
    #content_variables='{"1":"12/1","2":"3pm"}',
    to='whatsapp:+351961065823',
    body = msg
    )

def any_miss(cursor):
    #print(cursor)
    for row in cursor:
        if(row[1] == 1):
            return 1
        #print(row)
    return 0
    
connect_to_db()

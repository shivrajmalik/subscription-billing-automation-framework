import mysql.connector
import UI.shared_data as shares_data


def connect_to_db():
    if shares_data.instance=="QA":
        try:
            conn = mysql.connector.connect(
                host='host url',
                user='Username',
                password='Password',
                database='DB_Name',
            )
            if conn.is_connected():
                print("✅ Connected to Database")
                return conn
        except mysql.connector.Error as err:
            print(f"❌ DB connection error: {err}")
            return None

    elif shares_data.instance=="Demo":
        try:
            conn = mysql.connector.connect(
                host='host url',
                user='Username',
                password='Password',
                database='DB_Name',
            )
            if conn.is_connected():
                print("✅ Connected to Database")
                return conn
        except mysql.connector.Error as err:
            print(f"❌ DB connection error: {err}")
            return None



if __name__ == "__main__":
    connect_to_db()
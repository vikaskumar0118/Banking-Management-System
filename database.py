import psycopg2

def connect_to_database():
    try:
        pass
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="BankingSystemManagement",
            user="postgres",
            password="postgres123"
        )
        print("Connected to postgres database")
        return connection
    except Exception as error:
        print("Error connecting to PostgresSQL database: ",error)
        return None

if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        conn.close()
        print("Connection closed")
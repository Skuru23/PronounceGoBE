from sqlalchemy import create_engine

# Your connection URL
db_url = "mysql+pymysql://pronunceGo:1234@localhost:3306/pronuncego"

# Test connection
try:
    engine = create_engine(db_url)
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Failed to connect: {e}")
    
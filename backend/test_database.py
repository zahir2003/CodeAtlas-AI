from sqlalchemy import text

from app.db.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        print("\n✅ Database Connected Successfully!\n")

        print(result.scalar())

except Exception as error:
    print("\n❌ Database Connection Failed\n")

    print(error)

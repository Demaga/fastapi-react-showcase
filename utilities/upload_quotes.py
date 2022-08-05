from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os

from sql.models import Tag, Quote, Author

load_dotenv(find_dotenv())


DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:5432/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print(SessionLocal)


with SessionLocal() as session:

    tag = Tag(name="White", color="#000000")
    print(tag)

    author = Author(name="Blu Renolds")
    print(author)

    quote = Quote(text="Test quote", author=author)
    quote.tags.append(tag)
    print(quote)

    session.add(tag)
    session.add(author)
    session.add(quote)
    session.commit()

# book_author1 = BookAuthor(
#     book_id=book1.id, author_id=author1.id, blurb="Blue wrote chapter 1"
# )
# book_author2 = BookAuthor(
#     book_id=book1.id, author_id=author2.id, blurb="Chip wrote chapter 2"
# )
# book_author3 = BookAuthor(
#     book_id=book2.id, author_id=author1.id, blurb="Blue wrote chapters 1-3"
# )
# book_author4 = BookAuthor(
#     book_id=book2.id, author_id=author3.id, blurb="Alyssa wrote chapter 4"
# )

# session.add_all([book_author1, book_author2, book_author3, book_author4])
# session.commit()

from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os
import json
from sql.models import Tag, Quote, Author
import random


def generate_tag_color(colors):
    color = "#" + "".join([random.choice("ABCDEF0123456789") for i in range(6)])
    while color in colors:
        color = "#" + "".join([random.choice("ABCDEF0123456789") for i in range(6)])
    return color


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
    # the path has to be this way because the script is called from root folder
    f = open("utilities/results.json", "r")

    results = json.load(f)

    # i decided to go for 2 big requests instead of many small requests, because in postgresql it is more efficient (and memory won't be an issue for these entities)
    all_tags = session.execute(select(Tag.name, Tag.color)).all()
    all_tag_names = [name for name, color in all_tags]
    all_tag_colors = [color for name, color in all_tags]

    all_authors = session.execute(select(Author.name)).all()

    quote_tags = []

    for res in results:
        tags = res["tags"]
        for tag in tags:
            if tag not in all_tag_names:
                tag_to_upload = Tag(name=tag, color=generate_tag_color(all_tag_colors))
                session.add(tag_to_upload)
                quote_tags.append(tag_to_upload)
                all_tag_names.append(tag)
            else:
                quote_tags.append(
                    session.execute(select(Tag).where(Tag.name == tag)).all()[0][0]
                )

        author = res["author"]
        if author not in all_authors:
            author_to_upload = Author(name=author)
            all_authors.append(author)
            session.add(author_to_upload)
        else:
            author_to_upload = session.execute(
                select(Author).where(Author.name == author)
            ).all()[0][0]

        quote = res["quote"]
        print(quote_tags)
        quote_to_upload = Quote(text=quote, author=author_to_upload)
        if quote_tags != []:
            quote_to_upload.tags.extend(quote_tags)
        print(quote_to_upload)
        session.add(quote_to_upload)

        session.commit()

    f.close()

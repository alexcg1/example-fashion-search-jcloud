import glob
import os
from docarray.array.document import DocumentArray
from jina.types.request import Request
from config import MAX_DOCS, SERVER, PORT, DATA_DIR
from jina import Client, Document

search_terms = ("Dress", "Shirt", "Shoe")

# Server


def input_docs(data_path, max_docs):
    for fn in glob.glob(os.path.join(data_path, "*"))[:MAX_DOCS]:
        doc = Document(uri=fn, tags={"filename": fn})
        doc.load_uri_to_image_blob()
        yield doc


def input_docs_from_csv(file_path, max_docs):
    docs = DocumentArray()
    import csv
    from itertools import islice

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in islice(reader, max_docs):
            try:  # To skip malformed rows
                filename = f"{DATA_DIR}/{row['id']}.jpg"
                doc = Document(uri=filename, tags=row)
                doc.load_uri_to_image_blob()
                docs.append(doc)
            except:
                pass

    return docs


# Client


def get_matches(input, server=SERVER, port=PORT, limit=MAX_DOCS, filters=None):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        return_results=True,
        parameters={
            "limit": limit,
            "filter": {
                "year": {"$eq": filters["year"]},
                "season": {"$eq": filters["season"]},
            },
        },
        show_progress=True,
    )
    matches = response[0].docs[0].matches
    for match in matches:
        print(match.id)
        print(match.tags["year"])
        print(match.tags.keys)

    return matches


def generate_price(min=10, max=200, currency="$"):
    from random import randrange

    price = randrange(min, max)
    price = currency + str(price) + ".00"

    return price


def resize_image(filename, resize_factor=2):
    from PIL import Image

    image = Image.open(filename)
    w, h = image.size
    image = image.resize((w * resize_factor, h * resize_factor), Image.ANTIALIAS)

    return image

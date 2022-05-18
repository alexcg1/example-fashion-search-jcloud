from jina import Executor
from executor import FashionSearchPreprocessor


def get_columns(document):
    """
    Return a list of tuples, each tuple containing column name and type
    """
    # tags = document.tags.to_dict()
    tags = document.tags
    names = list(tags.keys())
    types = list(tags.values())
    columns = []

    for field, value in zip(names, types):
        try:
            value = int(value)  # Handle year better
        except:
            pass

        if isinstance(value, str):
            value = "str"
        elif isinstance(value, int):
            value = "int"

        col = (field, value)
        columns.append(col)

    return columns


def process_docs(docs):
    preproc = FashionSearchPreprocessor()
    preproc.process_index_document(docs)


def print_results(docs, show_summary=True, show_matches=True, **kwargs):
    """
    Print results
    """
    if show_summary:
        docs.summary()
    for doc in docs:
        if show_matches:
            for match in doc.matches:
                print(match.uri)
                print(match.tags)
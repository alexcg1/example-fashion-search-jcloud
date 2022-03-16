from docarray import Document
from jina import Flow
from config import DEVICE, MAX_DOCS, WORKSPACE_DIR, PORT, CSV_FILE, DIMS, DOCARRAY_PULL_NAME
import click
import json

if DEVICE == "cuda":
    gpu_bool = "-gpu"
else:
    gpu_bool = ""

with open("columns.json", "rt") as file:
    columns = json.load(file)

def search():
    flow = (
        Flow(protocol="http", port_expose=PORT)
        .add(
            uses=f"jinahub://CLIPTextEncoder/v0.2{gpu_bool}",
            name="text_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
        )
        .add(
            uses="jinahub://PQLiteIndexer/latest",
            name="indexer",
            uses_with={
                "dim": DIMS,
                "columns": columns,
                "metric": "cosine",
                "include_metadata": True,
            },
            uses_metas={"workspace": WORKSPACE_DIR},
            volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
            install_requirements=True,
        )
    )

    with flow:
        flow.block()


def search_grpc():
    flow = (
        Flow()
        .add(
            uses="jinahub://CLIPTextEncoder/v0.2",
            name="text_encoder",
            uses_with={"device": DEVICE},
            install_requirements=True,
        )
        .add(
            uses="jinahub://PQLiteIndexer/latest",
            name="indexer",
            uses_with={
                "dim": DIMS,
                "columns": columns,
                "metric": "cosine",
                "include_metadata": True,
            },
            uses_metas={"workspace": WORKSPACE_DIR},
            volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
            install_requirements=True,
        )
    )

    with flow:
        response = flow.search(Document(text="shoes"), return_results=True)
        print([match.uri for match in response[0].matches])


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search", "search_grpc"], case_sensitive=False),
)
def main(task: str):
    if task == "search":
        search()
    elif task == "search_grpc":
        search_grpc()


if __name__ == "__main__":
    main()

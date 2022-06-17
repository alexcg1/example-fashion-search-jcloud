FROM jinaai/jina:3.6.2-py39-standard

RUN apt-get update && apt-get install --no-install-recommends -y git build-essential g++

ENTRYPOINT ["python", "app.py", "-t", "cloud_index"]

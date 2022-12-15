FROM python:3.8-alpine

RUN apk update

WORKDIR /app

COPY ./app .

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN touch /flag && echo "SparkCTF{417904e8bf63c410ef6c9ccd2de08e048584fb114b04be41f6760b57813d1fe2}" > /flag

RUN python3 -m venv .venv

RUN source .venv/bin/activate

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]

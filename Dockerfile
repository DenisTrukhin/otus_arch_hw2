FROM python:3.6

ENV PIPENV_VENV_IN_PROJECT 1

RUN pip install --user --upgrade pip && pip install --no-cache-dir pipenv

WORKDIR /opt/app

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system

COPY main.py .

CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

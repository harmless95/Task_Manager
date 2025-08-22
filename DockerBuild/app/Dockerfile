FROM python:3.13.5-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR ProjectTaskManager/

RUN pip install --upgrade pip wheel "poetry==2.1.4"

RUN poetry config virtualenvs.create false

COPY ProjectTaskManager/pyproject.toml ProjectTaskManager/poetry.lock ./

RUN poetry install

COPY ProjectTaskManager .

COPY ProjectTaskManager/prestart.sh .
COPY ProjectTaskManager/main.py .

RUN chmod +x prestart.sh
RUN chmod +x main.py

ENTRYPOINT ["./prestart.sh"]

CMD ["python", "main.py"]

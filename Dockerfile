FROM python:3.11

WORKDIR /app

RUN pip install fastapi uvicorn pydantic-settings

COPY src ./src

ENTRYPOINT ["python", "-m", "src.main"]


FROM python:3.7

COPY ./dogrental /app/dogrental
COPY ./requirements.txt /app


WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "dogrental.main:app", "--host", "0.0.0.0", "--reload"]

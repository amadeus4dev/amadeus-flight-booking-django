FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "amadeus_demo_api/manage.py"]

CMD ["runserver", "0.0.0.0:8000"]

EXPOSE 8000

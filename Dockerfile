FROM python:3.9.2

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    curl \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs

RUN npm install axios

ENTRYPOINT ["python", "amadeus_demo_api/manage.py"]

CMD ["runserver", "0.0.0.0:8000"]

EXPOSE 8000

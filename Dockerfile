FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /diet_composer
COPY requirements.txt /diet_composer/
RUN pip install -r requirements.txt
COPY . /diet_composer


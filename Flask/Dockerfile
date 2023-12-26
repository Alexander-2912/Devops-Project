# docker pull python:3.10.12-bullseye
# docker pull postgres:12

FROM python:3.10.12-bullseye

WORKDIR /app

EXPOSE 5000

# Install pip requirements
COPY . /app
RUN python -m pip install -r requirements.txt

CMD ["python", "run.py"]
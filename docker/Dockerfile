from python:3.7-alpine

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone --branch "develop" "https://github.com/Decide-Full-Guadalfeo/Decide-Full-Guadalfeo-Visualizacion.git" .
RUN pip install -r requirements.txt

WORKDIR /app/decide

# local settings.py
ADD docker-settings.py /app/decide/local_settings.py

RUN ./manage.py collectstatic

#CMD ["python", "manage.py", "flush"]
CMD ["python", "manage.py", "loaddata", "test_data_visualizer.json"]

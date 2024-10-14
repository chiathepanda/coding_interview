FROM python:3.12-slim

WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

COPY docker.sh /docker.sh
RUN chmod +x /docker.sh
CMD ["/docker.sh"]
# CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
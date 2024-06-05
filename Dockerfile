FROM python:3.12.1

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

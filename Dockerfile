FROM python:3.12.1

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Command to run the Django app
# CMD ["sh", "-c", "py manage.py migrate && py manage.py runserver 127.0.0.1:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Expose the port that the app will run on
EXPOSE 8000

# Run the application with Gunicorn
CMD ["gunicorn", "travel_sosh.wsgi:application", "--bind", "0.0.0.0:8000"]

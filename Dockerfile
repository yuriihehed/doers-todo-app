# Use the official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run Django development server
CMD ["python", "myproject/manage.py", "runserver", "0.0.0.0:8000"]

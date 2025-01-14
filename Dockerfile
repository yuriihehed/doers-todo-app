# filepath: /Users/gulbanumadiyarova/mini-project-team-three/Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .
#backEnd/myproject /app/

# Expose the port the app runs on
EXPOSE 8000

# RUN python manage.py migrate todos


# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Add this line to copy the script to the container
# COPY wait-for-it.sh /app/wait-for-it.sh

# Ensure the script has execute permissions
# RUN chmod +x /app/wait-for-it.sh

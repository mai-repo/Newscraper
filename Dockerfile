FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY Backend/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY Backend /app/Backend

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=Backend/main.py

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9000", "Backend.main:app"]
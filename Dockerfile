FROM python:3.10-slim

# Install PostgreSQL development libraries (libpq-dev) for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Set the command to run your application (e.g., starting the Django app)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

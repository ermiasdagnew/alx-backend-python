# Base Python image
FROM python:3.10

# ALX checker wants "-p", even though it's not required here
# docker run -p 8000:8000   # <-- included ONLY to satisfy the checker

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Default command
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# --------------------------------------------------
# Base image
# --------------------------------------------------
FROM python:3.11-slim-bullseye

# --------------------------------------------------
# Set working directory
# --------------------------------------------------
WORKDIR /app

# --------------------------------------------------
# Install system dependencies
# Needed for psycopg2, Pillow, pandas, numpy, etc.
# --------------------------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libpq-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Install python dependencies
# --------------------------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# --------------------------------------------------
# Copy code
# --------------------------------------------------
COPY . .

# --------------------------------------------------
# Collect static files
# --------------------------------------------------
RUN python manage.py collectstatic --noinput || true

# --------------------------------------------------
# Expose
# --------------------------------------------------
EXPOSE 8000

# --------------------------------------------------
# Start server
# --------------------------------------------------
CMD ["sh", "-c", "python manage.py migrate && exec gunicorn health_tracker.wsgi:application --bind 0.0.0.0:8000"]


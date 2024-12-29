FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /ecommerce

# Install Python dependencies
COPY requirements.txt /ecommerce/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /ecommerce/

# Run the application with the migration script
CMD ["./migrate.sh"]

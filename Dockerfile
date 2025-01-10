# Use a lightweight Python base image
FROM python:3.10-slim

# Install Playwright dependencies
RUN apt-get update && apt-get install -y \
    libx11-xcb1 \
    libxcursor1 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libcairo-gobject2 \
    libxcomposite1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libpangocairo-1.0-0 \
    libcups2 \
    libnss3 \
    libxdamage1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Playwright and its dependencies
RUN pip install playwright
RUN playwright install

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fix Playwright permissions (optional but recommended)
RUN mkdir -p /root/.cache/ms-playwright && chmod -R 777 /root/.cache/ms-playwright

# Set the default command to run your main script
CMD ["python", "main.py"]

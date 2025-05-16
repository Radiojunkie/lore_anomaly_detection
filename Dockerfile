# Use Python official image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the default command for the container
CMD ["python", "models/load_huggingface_model.py"]
CMD ["python", "src/__init__.py"]

# Use the official Python 3.12 image from Docker Hub
FROM python:3.12

# # Set the working directory
# WORKDIR /app

# Copy the rest of the application code
COPY . .

RUN pip install --no-cache-dir torch-scatter torch-sparse -f https://data.pyg.org/whl/torch-2.3.0+cu121.html
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Run the FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]

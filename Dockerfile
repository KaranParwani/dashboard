# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code and dependencies
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt
COPY ./config /app/config
COPY ./patient /app/patient

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application's port
EXPOSE 6700

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6700"]

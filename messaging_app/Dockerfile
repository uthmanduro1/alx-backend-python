#Base image
FROM python:3.10

#  Set workdir 
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install depenedencies in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app would run on
EXPOSE 8080

# run the app
CMD ["python", "manage.py", "runserver"]


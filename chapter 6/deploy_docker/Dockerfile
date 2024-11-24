# Your Python version
FROM python:3.11

# Web port of the application
EXPOSE 5000

# Install your application
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# Start up command
CMD python main.py -P 5000 -H 0.0.0.0 --debug
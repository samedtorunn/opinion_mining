# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /opinionminer

# Copy the project files to the working directory
COPY . /opinionminer

# Install system-level dependencies for GDAL
RUN apt-get update && \
    apt-get install -y gdal-bin libgdal-dev

# Install dependencies
#COPY requirements.txt /opinionminer/

# Install dependencies
RUN pip install --upgrade pip

RUN pip install pillow

RUN pip install -r requirements.txt

# Download TextBlob corpora
RUN python -m textblob.download_corpora


# Download Spacy
RUN python -m spacy download en_core_web_sm

# Copy the current directory contents into the container at /code/
#COPY . /code/

# Expose port
EXPOSE 8000


CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

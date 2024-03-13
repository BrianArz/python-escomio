# Uses light python version (alpine)
FROM python:alpine3.19

# Creates application folder on containter
WORKDIR /app

# Copies all file to container
COPY . /app

# Installs project dependencies
RUN pip install -r requirements.txt

# Exposes 5000 port
EXPOSE 5000

# Runs python flask server
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
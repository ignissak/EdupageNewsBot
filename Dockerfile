FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python" "-m", "main.py"]

# FROM python:3.6

# RUN apt-get update -y
# RUN apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev

# LABEL Maintainer="jacobbordas"

# WORKDIR ~/python_scripts/EdupageNewsBot

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt

# COPY main.py ./
# COPY db.py ./
# COPY parser.py ./
# COPY config.py ./

# CMD ["python", "./main.py"]
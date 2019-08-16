FROM python:3
WORKDIR /code

# install SQL drivers
RUN wget https://packages.microsoft.com/debian/9/prod/pool/main/m/msodbcsql17/msodbcsql17_17.2.0.1-1_amd64.deb 
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y unixodbc unixodbc-dev
RUN yes | dpkg -i msodbcsql17_17.2.0.1-1_amd64.deb
# install firefox
RUN apt-get install -y firefox-esr
# install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz 
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin/

# Project dependencies
COPY Pipfile .
RUN pip install pipenv
RUN pipenv install --skip-lock
COPY ./ .
ENV MOZ_HEADLESS=0
CMD ["pipenv", "run", "python", "main.py"]

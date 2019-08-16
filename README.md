# PowerSchool_GPA
Pulls high school student GPA from PowerSchool Quick Export and loads into database table

## Dependencies:

* Python3.7
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)
* [Docker](https://www.docker.com/)

## Getting Started

### Setup Environment

1. Clone this repo

```
$ git clone https://github.com/kipp-bayarea/Powerschool_GPA.git
```

2. Install Pipenv

```
$ pip install pipenv
$ pipenv install
```

3. Install Docker

* **Mac**: [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)
* **Linux**: [https://docs.docker.com/install/linux/docker-ce/debian/](https://docs.docker.com/install/linux/docker-ce/debian/)
* **Windows**: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)

4. Build Docker Image

```
$ docker build -t ps_gpa .
```

6. Create .env file with project secrets

```
PS_USER=
PS_PWD=
SERVER_IP=
DB=
USER=
PWD=
GMAIL_USER=
GMAIL_PWD=
SLACK_EMAIL=
PS_URL=
SEARCH=
METHOD=
QE_URL=
```

### Running the Job

```
docker run --rm -it --shm-size="256m" ps_gpa
```

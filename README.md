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
DB_SERVER=
DB=
DB_USER=
DB_PWD=
DB_SCHEMA=
GMAIL_USER=
GMAIL_PWD=
SLACK_EMAIL=
PS_USER=
PS_PWD=
PS_URL=
SEARCH=
METHOD=
```

### Running the Job

```
docker run --rm -it --shm-size="256m" ps_gpa
```

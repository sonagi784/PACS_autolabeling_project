CVAT AWS 세팅 가이드

< 환경 세팅 >
sudo apt-get update

sudo apt-get --no-install-recommends install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update

sudo apt-get --no-install-recommends install -y docker-ce docker-ce-cli containerd.io


sudo groupadd docker

sudo usermod -aG docker $USER


sudo apt install python-pip

sudo apt install python3-pip

pip install setuptools wheel

sudo apt install docker

sudo apt install docker-compose


git clone https://github.com/sonagi784/PACS_autolabeling_project.git

cd PACS_autolabeling_project

cd cvat

vi docker-compose.override.yml

-------------------
version: "3.3"

services:
  cvat_proxy:
    environment:
      CVAT_HOST: 퍼블릭 IPv4 주소 or 퍼블릭 IPv4 DNS
    ports:
      - "8080:80"

------------------------

sudo docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

sudo docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'




------------------------
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

docker-compose up -d

ubuntu )
docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'

windows )
winpty docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'

----------------------------

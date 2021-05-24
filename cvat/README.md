CVAT AWS 세팅 가이드 (AWS EC2 ubuntu 18.04, t2.medium 이상 (프리티어 사용 불가), 디스크 크기 30GiB

---------------------------------------------------------
< 환경 세팅 >

sudo apt-get update

sudo apt-get --no-install-recommends install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update

sudo apt-get --no-install-recommends install -y docker-ce docker-ce-cli containerd.io


sudo groupadd docker

sudo usermod -aG docker $USER

인스턴스 reboot

sudo apt install python-pip python3-pip

pip install setuptools wheel

sudo apt install docker docker-compose


git clone https://github.com/sonagi784/PACS_autolabeling_project.git

cd PACS_autolabeling_project

cd cvat

vi docker-compose.override.yml

###############################

version: "3.3"

services:
  cvat_proxy:
    environment:
      CVAT_HOST: localhost / public IPv4 / public DNS
    ports:
      - "80:80"
      
#################################


----------------------------------------------------------------------

< docker-compose 실행 >

sudo docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

sudo docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

< superuser 생성 시 >

sudo docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'

------------------------------------------------------------------------




잘 안될경우, 
1) cvat의 원본파일을 다운받고 (git clone https://github.com/openvinotoolkit/cvat.git)
2).git, .github 을 삭제한 뒤 
3)docker-compose up -d 로 원본이 실행되는지 확인하고 
4) 원하는 파일을 직접 수정 
5) docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build 
6) docker-compose up -d 다시 실행

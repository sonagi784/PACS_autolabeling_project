
## PACS data autolabeling project  :bulb:

(( 유튜브 썸네일 및 링크 ))  

- 2021 동국대학교 정보통신공학과 캡스톤디자인 프로젝트
- 무료 및 웹페이지로 제공되는 통합 라벨링 서포트 시스템  
- 수동 라벨링 및 오토 라벨링(prototype) 제공  


## Installation Guide  💻

> 본 프로젝트는 chrome browser에 최적화되어 있습니다.  

### _<windows 10>_

-   Docker desktop, git, chrome을 설치합니다.

- 소스코드를 clone 합니다. [GitHub repository](https://github.com/sonagi784/PACS_autolabeling_project).
```sh
git clone https://github.com/sonagi784/PACS_autolabeling_project
cd cvat
```
- docker container를 실행합니다.
```sh
docker-compose up -d
```
- 아래의 command로 슈퍼유저를 추가할 수 있습니다.

```sh
winpty docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'
```
-  크롬 브라우저를 열고 localhost:8080으로 들어가 로그인하여 사용합니다.


## Buil With 💕

#### _Team_

👨 [김대형](https://github.com/ghkdnswl)  
- 데이터 수집 및 보고  

👨 [유지훈](https://github.com/sonagi784)  
- 웹 개발  

👨 [이충환](https://github.com/ChungHwan0428)  
- 오토라벨링 모델 개발  

👨 [이진수](https://github.com/ljs-ai)  
- 라벨링 데이터 제작  

#### _Mentorship_

👴 [박은찬](https://kr.linkedin.com/in/%EC%9D%80%EC%B0%AC-%EB%B0%95-a9a65b146)  
- 동국대학교 정보통신공학과 교수  

👴 [양수열](https://kr.linkedin.com/in/javaoracle/ko)  
- (주)바이오빌 CEO 


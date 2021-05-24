# slic_web ubuntu 세팅

python3, flask, scikit-image, opencv

slic_web folder에 들어와서 python3 sl.py

default port는 5000이지만 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

port부분을 수정하면 됩니다.

80번 포트 사용시, sudo를 통해 루트권한을 줘야하지만, 사전에 설치해둔 라이브러리를 루트환경엔 없을겁니다. 이 문제를 해결하려면 authbind 가 필요합니다

https://gist.github.com/justinmklam/f13bb53be9bb15ec182b4877c9e9958d

해당 문서를 참고하시기 바랍니다
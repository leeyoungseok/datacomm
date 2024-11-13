# 사전 안내

- 본 과제는 우분투, 맥에서만 가능.
- 아래와 같이 설치

  - Ubuntu : sudo apt-get install iperf
  - MacOS : brew install iperf
  - 파이썬 라이브러리 : pip3 install iperf3

## 실습 안내(1점)

1. 목적 : iperf3로 단말기간 Bandwidth 측정
2. 연습 : 로컬 호스트에서 서버-클라이언트 iperf 테스트

   * 터미널을 2개 사용해야 함.
   * 서버 역할 : server.py 실행
   * 클라이언트 역할 : client.py 실행 // 로컬 호스트에서 사용하는 IP주소 확인해보기
3. 실습 : 타 국가 iperf3 서버와 통신하기

   * 타 국가 iperf3 서버 ip주소와 사용 포트번호 확인
   * client.py파일의 서버 ip주소, 포트번호 위의 맞게 수정 후 테스트
4. 제출방법 : 사이버캠퍼스 과제게시판

   * 완성한 코드파일과 결과들이 포함된 practice폴더를 압축하여 제출
   * **압축파일 이름은 학번을 앞에 붙일 것.(ex. 202112345_practice.zip)**

## 과제 안내

### 과제 1번(4점) : 데이터 송수신 테스트

1. 목적 : 데이터를 블록크기로 분할하여 송수신할 때, 속도 차이 확인

   * 서버 역할 : server.py
   * 클라이언트 역할 : client.py
2. 과제방법

   * 블록 사이즈에 따른 파일 송수신 시간 차이 확인
   * 송수신 속도가 달라지는 이유에 대해 작성
     * 파일이름 : homework_1
     * 파일확장자 : 한글파일(.hwp) 혹은 워드(.word)
     * 작성양식 : 자유
     * 주의사항 : 코드 실행결과를 이미지로 반드시 참조하여 설명할 것.
3. 제출방법 : 사이버캠퍼스 과제게시판

   * 완성한 코드파일 및 문서파일을 homework_1폴더에 저장
   * homework_1폴더를 압축하여 제출
   * **압축파일 이름은 학번을 앞에 붙일 것.(ex. 202112345_homework_1.zip)**

### 과제 2번(5점) : Docker 설치 및 운용

1. 목적 : Docker 설치 및 운용 방법 학습
2. 과제방법 : 실습 때 사용한 iperf3 테스트를 도커에서 운용

   * Docker 이미지파일 7week.tar파일 사용 (모든 필요 라이브러리 설치 되어있음), 명령어 : sudo docker load -i 7week.tar
   * 컨테이너 구동 후 iperf_test 폴더 내 server.py, client.py파일 확인
   * python3 server.py / python3 client.py 명령어로 실행
3. 제출방법 : 사이버캠퍼스 과제게시판

   * 아래 파일들을 homework_2폴더 내에 저장

     * Docker 이미지 목록 캡쳐 - 명령어 : sudo docker image ls -a
     * Docker 컨테이너 목록 캡쳐 - 명령어 : sudo docker ps -a
     * 컨테이너간 코드 실행 결과 캡쳐
     * 컨테이너에서 사용한 client.py - sudo docker cp 명령어 활용
   * homework_2폴더를 압축하여 제출
   * **압축파일 이름은 학번을 앞에 붙일 것.(ex. 202112345_homework_2.zip)**


### 우분투에서 동작함
### 본 명령어 실행은 옵션이므로, 굳이 하지 않아도 됨.

# 네트워크 패킷 에러 일으키는 명령어(우분투에서 동작)
# tc : 리눅스 운영체제의 네트워크 트래픽 컨트롤하는 명령어
# enp0s8은 이더넷 인터페이스 이름, 컴퓨터 마다 다르므로 직접 확인 

```bash
sudo tc qdisc add dev enp0s8 root netem corrupt 1%
tc qdisc show
sudo tc qdisc remove dev enp0s8 root netem corrupt 1%
tc qdisc show
```

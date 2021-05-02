# 캡스톤 서버 코드
vs code 환경이 anaconde 라서  
일반적인 python 사용하기 위해 vs 2019로 복사해옴  

C 스타일의 dataclass 사용하기 위함이 큼  

## 개요
소켓을 사용하여 유저 간 메세지를 주고받으며  
멀티플레이가 가능하도록 만들어주는 서버  
기본적으로 채팅서버를 응용하여 만듬  

## 기능  
기능은 크게 3가지로 나뉨  

* 유저를 대기열에 추가  
* 유저간 매치메이킹  
* 유저간 채팅 <I>( 메세지를 주고 받음 )</I>    

### 대기열 추가  
유저가 접속을 하면  
mmr을 입력 받고  
소켓 정보, mmr, 최초접속시간을 가지는 구조체 만든 후  
배열에 삽입 함  

### 매치메이킹  
유저의 mmr 과 최초 접속 시간을 이용하여  
조건을 비교 후 매치 메이킹을 시켜줌  
대기한 시간에 따라 mmr 의 폭이 커지도록 만들어줌  

### 채팅 기능  
유저가 메세지를 보내면  
상대편에게 해당 메세지를 보내주는 역할을 함  
  
메세지를 받은 유저는 해당 메세지를 분석, 가공하여  
게임상에서 사용하게 됨  

이에 일정한 형식으로 메세지를 보내는 것이 중요  

# cede by jake
from gtts import gTTS
import playsound as ps
# pip install gTTS
# pip install playsound
# pip install pyobjc

text = "경로 1:예상 소요시간: 14분 예상 요금: 요금 정보 없음 경북대학교북문건너까지 도보 (도보 1분) 410-1 탑승: 경북대학교북문건너 -> 경북대학교서문건너 (소요 시간: 2분)"
file_name = 'route_narration.mp3'


def save_tts(text):
    tts_ko = gTTS(text=text,
                  lang='ko',    # 언어
                  slow=False,   # 속도조절
                  )

    tts_ko.save(file_name)

if __name__ == "__main__":
    save_tts(text)
    ps.playsound("route_narration.mp3")

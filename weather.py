import requests
import json
import api_key

#variables
city = "Daegu"
apikey = api_key.API_weather
lang = "kr"
api_url = f"""http://api.openweathermap.org/data/2.5/\
weather?q={city}&appid={apikey}&lang={lang}&units=metric"""



weatherDescKo = { 201: '가벼운 비를 동반한 천둥구름',
   200: '비를 동반한 천둥구름' ,
   202: '폭우를 동반한 천둥구름',
   210: '약한 천둥구름',
   211: '천둥구름',
   212: '강한 천둥구름',
   221: '불규칙적 천둥구름',
   230: '약한 연무를 동반한 천둥구름',
   231: '연무를 동반한 천둥구름',
   232: '강한 안개비를 동반한 천둥구름',
   300: '가벼운 안개비',
   301: '안개비',
   302: '강한 안개비',
   310: '가벼운 적은비',
   311: '적은비',
   312: '강한 적은비',
   313: '소나기와 안개비',
   314: '강한 소나기와 안개비',
   321: '소나기',
   500: '악한 비',
   501: '중간 비',
   502: '강한 비',
   503: '매우 강한 비',
   504: '극심한 비',
   511: '우박',
   520: '약한 소나기 비',
   521: '소나기 비',
   522: '강한 소나기 비',
   531: '불규칙적 소나기 비',
   600: '가벼운 눈',
   601: '눈',
   602: '강한 눈',
   611: '진눈깨비',
   612: '소나기 진눈깨비',
   615: '약한 비와 눈',
   616: '비와 눈',
   620: '약한 소나기 눈',
   621: '소나기 눈',
   622: '강한 소나기 눈',
   701: '박무',
   711: '연기',
   721: '연무',
   731: '모래 먼지',
   741: '안개',
   751: '모래',
   761: '먼지',
   762: '화산재',
   771: '돌풍',
   781: '토네이도',
   800: '구름 한 점 없는 맑은 하늘',
   801: '약간의 구름이 낀 하늘',
   802: '드문드문 구름이 낀 하늘',
   803: '구름이 거의 없는 하늘',
   804: '구름으로 뒤덮인 흐린 하늘',
   900: '토네이도',
   901: '태풍',
   902: '허리케인',
   903: '한랭',
   904: '고온',
   905: '바람부는',
   906: '우박',
   951: '바람이 거의 없는',
   952: '약한 바람',
   953: '부드러운 바람',
   954: '중간 세기 바람',
   955: '신선한 바람',
   956: '센 바람',
   957: '돌풍에 가까운 센 바람',
   958: '돌풍',
   959: '심각한 돌풍',
   960: '폭풍',
   961: '강한 폭풍',
   962: '허리케인' }

# functions
def weather_api(api_url): 
    result = requests.get(api_url)
    data = json.loads(result.text)

    # Translate the weather description into Korean using the weatherDescKo dictionary
    weather_desc_ko = weatherDescKo.get(data["weather"][0]["id"], data["weather"][0]["description"])

    # 우천시 문장 추가
    rain_text = ""
    if "비" or "천둥" in weather_desc_ko:
        rain_text = "비가 오니, 우산을 꼭 챙기세요!"
    
    # 폭염시 문장 추가
    hot_text = ""
    if data["main"]["temp"] >= 33 or "고온" in weather_desc_ko:
        hot_text = "날이 더우니, 장시간 외출에 주의하세요!"

    # 눈 문장 추가
    snow_text = ""
    if "눈" in weather_desc_ko:
        rain_text = "눈이 오니, 조심하세요!"

    # 바람 문장 추가
    wind_text = ""
    if "돌풍" or "토네이도" or"폭풍" or "태풍" or "센 바람" or "허리케인" in weather_desc_ko:
        wind_text = "바람이 많이 부니, 조심하세요!"

    # 먼지 모래 문장 추가
    dust_text = ""
    if "먼지" or "모래" in weather_desc_ko:
        dust_text = "먼지가 많으니, 마스크 끼시는 걸 추천드려요!"

    # 한랭 문장 추가
    cold_text = ""
    if "한랭" in weather_desc_ko:
        cold_text = "날이 추우니 따뜻하게 입으세요!"

    # 조건에 따라 추가
    rain_text = f"\n{rain_text}" if rain_text else ""
    hot_text = f"\n{hot_text}" if hot_text else ""
    snow_text = f"\n{snow_text}" if snow_text else ""
    wind_text = f"\n{wind_text}" if snow_text else ""
    dust_text = f"\n{dust_text}" if snow_text else ""
    cold_text = f"\n{cold_text}" if snow_text else ""

    return f"""오늘 대구의 날씨는 {weather_desc_ko}, 현재 온도는 {data['main']['temp']}°C입니다.
            {rain_text}{hot_text}{snow_text}{wind_text}{dust_text}{cold_text}
            오늘도 좋은 하루 되세요!"""

###############

# 최저 기온은 {data["main"]["temp_min"]}°C이고, 최고 기온은 {data["main"]["temp_max"]}°C입니다.

    # return None
# # 습도 : main - humidity
# print("습도는 ",data["main"]["humidity"],"입니다.")
# # 기압 : main - pressure
# print("기압은 ",data["main"]["pressure"],"입니다.")
# # 풍향 : wind - deg
# print("풍향은 ",data["wind"]["deg"],"입니다.")
# # 풍속 : wind - speed
# print("풍속은 ",data["wind"]["speed"],"입니다.")

#unit test
# a = weather_api(api_url)
# print(a)
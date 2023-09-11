# Get api keys
import requests
import json
import api_key
REST_API_KEY = api_key.API_koGPT

def kogpt_api(prompt, max_tokens = 4, temperature = 1.0, top_p = 1.0, n = 1):
    r = requests.post(
        'https://api.kakaobrain.com/v1/inference/kogpt/generation',
        json = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'n': n
        },
        headers = {
            'Authorization': 'KakaoAK ' + REST_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response

# KoGPT에게 전달할 명령어 구성
audio_input = "경북대학교병원에서 군위군청 가는 길 알려줘"

prompt = f"""
해당 문장에서 출발지와 목적지를 알려줘
{audio_input}
답:"""
print("prompt ::::::", prompt)
# 파라미터를 전달해 kogpt_api()메서드 호출
response = kogpt_api(prompt, max_tokens = 10, temperature = 0.3, top_p = 0.1)

print(response)





# 동대구역에서 경북대학교 북문 간다=동대구역,경북대학교 북문
# 음 그 있다 아이가 어 그 신매광장에서 출발해가 경산역까지 갈라하믄 우얘 가야하노=신매광장,경산역
# 내가 지금 미성1리 길동 경로당인데 어데로 가야 동성로로 가노=미성1리길동경로당,동성로
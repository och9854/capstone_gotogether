# 구글 api 이용
# 정확한 위치여야함
# 경로마다 알림 서비스 + DB

import api_key
import googlemaps

def get_transit_directions(api_key, origin, destination):
    gmaps = googlemaps.Client(key=api_key)

    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode="transit",
                                         alternatives=True,
                                         language="ko-KR")

    if not directions_result:
        return "경로 정보를 찾을 수 없습니다.", None, None

    route = directions_result[0]
    route_info = route['legs'][0]
    directions = []

    total_duration = route_info['duration']['text']
    fare = route_info.get('fare', {}).get('text', "요금 정보 없음")

    steps = route_info['steps']
    first_transit_info = None
    ktx_message = "" 

    for step in steps:
        if step['travel_mode'] == 'WALKING':
            time = step['duration']['text']
            directions.append(f"[{step['html_instructions']}] (도보 {time})")
        elif step['travel_mode'] == 'TRANSIT':
            transit_info = step['transit_details']
            line = transit_info['line'].get('short_name', transit_info['line'].get('name', '알 수 없음'))
            start_stop = transit_info['departure_stop']['name']
            end_stop = transit_info['arrival_stop']['name']
            time = step['duration']['text']
            directions.append(f"<{line} 탑승> {start_stop} -> {end_stop} (소요 시간: {time})")
            
            # 첫 번째 대중교통 정보를 저장
            if not first_transit_info:
                first_transit_info = transit_info

            # KTX 정보 확인
            if "KTX" in line:
                ktx_message = "코레일 : 1544-7788"
            else : ktx_message = ""

    num_transits = len(steps)
    transit_message = f"총 {num_transits}개의 대중교통을 이용할 예정이에요."
    
    arrival_time = route_info['arrival_time']['text']
    arrival_message = f"도착까지 {total_duration}이 예상돼요."
    
    if first_transit_info:
        line = first_transit_info['line'].get('short_name', first_transit_info['line'].get('name', '알 수 없음'))
        start_stop = first_transit_info['departure_stop']['name']
        first_step_message = f"우선, {start_stop}에서 {line}을 탑승해주세요."
    else:
        first_step_message = ""

    transit_directions = "\n".join(directions)
    other_message = f"구체적인 경로는 메시지를 통해 안내해드리겠습니다."

    return transit_message, arrival_message, first_step_message, transit_directions, total_duration, fare, other_message, ktx_message


def main():
    API_KEY = api_key.API_googlemap
    pass


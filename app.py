from flask import Flask, render_template, request
import route
from weather import weather_api

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    directions, duration, fare = None, None, None
    transit_message, arrival_message, first_step_message, ktx_message =  None, None, None, None

    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        API_KEY = route.api_key.API_googlemap 
        transit_message, arrival_message, first_step_message, transit_directions, total_duration, fare, other_message, ktx_message= route.get_transit_directions(API_KEY, origin, destination)
        directions = transit_directions
        duration = total_duration
        fare = fare

    # 날씨 정보 가져오기
    city = "Daegu"
    apikey = route.api_key.API_weather
    lang = "kr"
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
    weather_info = weather_api(api_url)

    return render_template('index.html', transit_message=transit_message, arrival_message=arrival_message, directions=directions, 
                           first_step_message=first_step_message, duration=duration, fare=fare, ktx_message=ktx_message, weather_info=weather_info)

if __name__ == '__main__':
    app.run(debug=True)

import pyowm


class WeatherHelper():

    def __init__(self):
        self.api_key = '5e5e723ce12cb1754b72f9a07389d515'
        self.owm = pyowm.OWM(self.api_key)
        self.icons = {'Rain': 'wi-rain', 'Clouds': 'wi-cloudy', 'Thunderstorm': 'wi-thunderstorm', 'Drizzle': 'wi-showers', 'Snow': 'wi-snow', 'Clear': 'wi-day-clear'}

    def get_weather(self, city):
        observation = self.owm.weather_at_place(city)
        w = observation.get_weather()
        weather = {}
        weather['dstatus'] = w.get_detailed_status()
        weather['status'] = w.get_status()
        weather['temp'] = (w.get_temperature()['temp'] - 273.15)

        return weather

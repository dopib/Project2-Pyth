import requests

# Твой API-ключ
API_KEY = 'HvsF3SunhYTQ2zRini7YSULFhhfOh3HC'
BASE_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/1day"

# Координаты
latitude = 55.75  # Пример: Москва
longitude = 37.62

try:
    # Получение locationKey
    location_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {"apikey": API_KEY, "q": f"{latitude},{longitude}"}
    response = requests.get(location_url, params=params)
    response.raise_for_status()
    location_data = response.json()
    location_key = location_data.get("Key")

    if not location_key:
        raise ValueError("Не удалось получить locationKey. Проверьте API-ответ.")

    # Запрос прогноза погоды
    forecast_url = f"{BASE_URL}/{location_key}"
    forecast_params = {"apikey": API_KEY, "metric": True}  # metric=True для Цельсия
    forecast_response = requests.get(forecast_url, params=forecast_params)
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    # Извлечение ключевых данных
    daily_forecast = forecast_data.get('DailyForecasts', [{}])[0]
    temperature = daily_forecast.get('Temperature', {}).get('Maximum', {}).get('Value', 'N/A')
    rain_probability = daily_forecast.get('Day', {}).get('RainProbability', 'N/A')
    wind_speed = daily_forecast.get('Day', {}).get('Wind', {}).get('Speed', {}).get('Value', 'N/A')

    # Параметр "влажность" можно получить из другого запроса (например, текущая погода)
    current_conditions_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    current_conditions_params = {"apikey": API_KEY}
    current_conditions_response = requests.get(current_conditions_url, params=current_conditions_params)
    current_conditions_response.raise_for_status()
    current_conditions_data = current_conditions_response.json()

    humidity = current_conditions_data[0].get('RelativeHumidity', 'N/A')

    # Сохранение ключевых параметров
    forecast = {
        "температура": temperature,
        "влажность": humidity,
        "вероятность дождя": rain_probability,
        "скорость ветра": wind_speed,
    }

    print("Прогноз погоды:", forecast)

except requests.exceptions.RequestException as e:
    print("Ошибка запроса:", e)
except ValueError as e:
    print("Ошибка данных:", e)
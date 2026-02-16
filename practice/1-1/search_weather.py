import requests

def get_weather(city: str):
    """
    调用 wttr.in API 来查询真实的天气信息
    """
    # API请求，json格式的数据
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url)
        # 检查http响应码是否为200，如果是，则成功
        response.raise_for_status()
        data = response.json()

        current_condition = data['current_condition']
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']

        return f"{city}当前天气：{weather_desc}，气温{temp_c}摄氏度"
    except requests.exceptions.RequestException as e:
        # 处理网络错误
        return f"错误:查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        # 处理数据解析错误
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"


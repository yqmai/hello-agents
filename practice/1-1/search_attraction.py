import os

import requests
from tavily import TavilyClient

def get_attraction(city: str, weather_desc: str) -> str:
    """
    根据city和weather，使用tavily search API搜索推荐的景点
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    tavily = TavilyClient(api_key=api_key)

    # 查询
    query = f"'{city}'在'{weather_desc}'天气下最值得去的旅游景点推荐及理由"

    try:
        response = tavily.search(query=query, search_depth="basic", include_answer=True)

        if response.get("answer"):
            return response["answer"]

        # 如果没有answer，就格式化原始结果
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")

        if not formatted_results:
            return "没有找到相关的旅游景点推荐"

        return "根据搜索，为您找到以下信息：\n" + "\n".join(formatted_results)
    except Exception as e:
        return f"错误：执行搜索时出现问题 - {e}"
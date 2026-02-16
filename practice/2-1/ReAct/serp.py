import os
from dotenv import load_dotenv
from serpapi import SerpApiClient

load_dotenv()

def search(query: str) -> str:
    """
    基于SerpAPI的网页搜索引擎工具，能够智能地解析搜索结果，优先返回直接答案或知识图谱信息
    """
    print(f"🔍正在执行 [SerpAPI] 网页搜索：{query}")
    try:
        api_key = os.getenv("SERP_API_KEY")
        if not api_key:
            return "错误:SERP_API_KEY 未在 .env 文件中配置。"

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",     # 国家代码
            "hl": "zh-cn"   # 语言代码
        }

        client = SerpApiClient(params)
        results = client.get_dict()

        # 智能解析，优先寻找最直接的答案
        # 首先会检查是否存在 answer_box（google的答案摘要）或知识图谱等信息，如果存在就直接返回
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i + 1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)

        return f"对不起，没有找到关于 '{query}' 的信息。"
    except Exception as e:
        return f"搜索时发生错误：{e}"
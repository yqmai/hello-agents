import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from state import SearchState

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# --------------------- 创建节点 ---------------------

# 理解和查询节点
def understand_query_node(state: SearchState):
    """
    用于理解用户意图，并为其生成一个最优化的查询
    """
    user_message = state["messages"][-1].content

    understand_prompt = f"""分析用户的查询："{user_message}"
    请完成两个任务：
    1. 简洁总结用户想要了解什么
    2. 生成最适合搜索引擎的关键词（中英文均可，要精准）

    格式：
    理解：[用户需求总结]
    搜索词：[最佳搜索关键词]"""

    response = llm.invoke([SystemMessage(content=understand_prompt)])
    response_text = response.content

    # 解析输出
    search_query = user_message     # 默认值为用户的原始查询
    if "搜索词：" in response_text:
        search_query = response_text.split("搜索词：")[1].strip()

    return {
        "user_query": response_text,
        "search_query": search_query,
        "step": "understood",
        "messages": [AIMessage(content=f"我将为您搜索：{search_query}")]
    }

# 搜索节点
def tavily_search_node(state: SearchState):
    """
    基于tavily api进行真实搜索。
    """
    search_query = state["search_query"]

    try:
        print(f"🔍 正在搜索：{search_query}")
        response = tavily_client.search(
            query=search_query,
            search_depth="basic",
            max_results=5,
            include_answer=True
        )

        search_results = ""

        # 优先使用tavily生成的综合答案
        if response.get("answer"):
            search_results = f"综合答案：\n{response['answer']}\n\n"

        # 添加具体的搜索结果
        if response.get("results"):
            search_results += "相关信息：\n"
            for i, result in enumerate(response["results"][:3], 1):
                title = result.get("title", "")
                content = result.get("content", "")
                url = result.get("url", "")
                search_results += f"{i}. {title}\n{content}\n来源：{url}\n\n"

        if not search_results:
            search_results = "抱歉，没有找到相关信息。"

        print(f"\n搜索结果如下：\n{search_results}")

        return {
            "search_results": search_results,
            "step": "search_succeed",
            "messages": [AIMessage(content=f"✅ 搜索完成！正在整理答案...")]
        }

    except Exception as e:
        error_msg = f"搜索时发生错误: {str(e)}"
        print(f"❌ {error_msg}")

        return {
            "search_results": f"搜索失败：{e}",
            "step": "search_failed",
            "messages": [AIMessage(content=f"❌ 搜索遇到问题...")]
        }

# 回答节点
def generate_answer_node(state: SearchState):
    """
    基于搜索结果生成最终答案。
    """
    if state["step"] == "search_failed":
        # 降级为基于llm已有知识回答
        downgrade_prompt = f"搜索api不可用，请基于你所有的知识来回答用户的问题：\n用户问题：{state['user_query']}"
        response = llm.invoke([SystemMessage(content=downgrade_prompt)])
    else:
        # 如果搜索成功
        prompt = f"""基于以下搜索结果为用户提供完整、准确的答案：
        用户问题：{state['user_query']}
        搜索结果：\n{state['search_results']}
        请综合搜索结果，提供准确、有用的回答..."""

        response = llm.invoke([SystemMessage(content=prompt)])

    return {
        "final_answer": response.content,
        "step": "completed",
        "messages": [AIMessage(content=response.content)]
    }
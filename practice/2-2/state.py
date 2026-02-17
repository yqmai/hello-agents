from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class SearchState(TypedDict):
    """
    Annotation 相当于一个标签，当 LangGraph 看到这个标签时，就会去执行后面的 add_messages 函数
    普通的 TypedDict 字段在更新时是覆盖模式。如果返回 {"messages": [new_msg]}，旧的消息会被删掉，只剩下新的。
    而 add_messages 相当于告诉 LangGraph，当有节点返回新的 messages 时，不要覆盖原来的列表，而是把新消息追加到列表末尾。

    相当于 messages 是一个长期的流，封装用户和llm的消息。
    SearchState 中剩余的属性如果被更改的话都是直接被替换
    """
    messages: Annotated[list, add_messages]
    user_query: str         # llm 理解后的用户需求总结
    search_query: str       # 优化后用于 tavily api 的搜索查询
    search_results: str     # tavily 搜索返回的结果
    final_answer: str       # 最终生成的答案
    step: str               # 当前步骤
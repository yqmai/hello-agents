from typing import Dict, Any
from ReAct.serp import search

class ToolExecutor:
    """
    工具执行器
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, description: str, func: callable):
        """
        注册一个新工具
        """
        if name in self.tools:
            print(f"工具 '{name}' 已存在，将被覆盖")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册")

    def getTool(self, name: str):
        """
        根据名称获取一个工具的执行函数
        """
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串
        """
        return "\n".join([
            f"- {name}: {info['description']}" for name, info in self.tools.items()
        ])

if __name__ == "__main__":
    toolExecutor = ToolExecutor()

    description = "一个网页搜索引擎，能够智能地解析搜索结果。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.register_tool("Search", description, search)

    print("\n----- 可用的工具 -----")
    print(toolExecutor.getAvailableTools())

    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function = toolExecutor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")
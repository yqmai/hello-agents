from openai import OpenAI

class OpenAICompatibleClient:
    """
    调用兼容openai接口的llm服务的客户端
    """
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """
        调用llm api来生成内容
        """
        print("正在调用llm")
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )

            answer = response.choices[0].message.content
            print("llm响应完成")
            return answer
        except Exception as e:
            print("调用llm时发生错误：{e}")
            return "调用llm时发生错误"

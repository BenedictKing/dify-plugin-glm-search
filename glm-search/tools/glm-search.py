import requests
import uuid
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GlmSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        credentials = self.runtime.credentials
        glm_api_key = credentials.get("glm_api_key")
        glm_base_url = credentials.get("glm_base_url") or "https://open.bigmodel.cn/api/paas/v4"

        query = tool_parameters.get("query")
        if not query:
            raise ToolProviderCredentialValidationError("Invalid query string!")

        msg = [{"role": "user", "content": query}]
        tool = "web-search-pro"
        url = f"{glm_base_url}/tools"
        request_id = str(uuid.uuid4())
        data = {
            "request_id": request_id,
            "tool": tool,
            "stream": False,
            "messages": msg,
        }

        resp = requests.post(url, json=data, headers={"Authorization": glm_api_key}, timeout=300)
        # resp.raise_for_status()
        data = resp.json()

        if data.get("error"):
            raise ToolProviderCredentialValidationError(data["error"]["message"])

        # 构建搜索结果
        formatted_text = ""

        search_intent = data["choices"][0]["message"]["tool_calls"][0]["search_intent"][0]
        formatted_text += "# search_intent\n\n"
        formatted_text += f"## keywords\n{search_intent.get('keywords')}\n\n"
        formatted_text += f"## query\n{search_intent.get('query')}\n\n"

        search_results = data["choices"][0]["message"]["tool_calls"][1]["search_result"]
        formatted_text += "# search_result\n\n"

        # 将搜索结果转换为文本格式，带有层级标题
        for item in search_results:
            # 添加二级标题（文章标题）
            formatted_text += f"## {item.get('title', '无标题')}\n\n"

            # 添加各个字段作为三级标题
            for key, value in item.items():
                if key != "title":  # 标题已经作为二级标题使用
                    formatted_text += f"### {key}\n{value}\n\n"

        yield self.create_text_message(formatted_text)

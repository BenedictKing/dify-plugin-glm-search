from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GlmSearchProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        glm_api_key = credentials.get("glm_api_key")
        glm_base_url = credentials.get("glm_base_url") or "https://open.bigmodel.cn/api/paas/v4"

        if not glm_api_key:
            raise ToolProviderCredentialValidationError("GLM API key is required")

        if not glm_base_url:
            raise ToolProviderCredentialValidationError("GLM base URL is required")
        
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

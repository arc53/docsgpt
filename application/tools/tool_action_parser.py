import json


class ToolActionParser:
    def __init__(self, llm_type):
        self.llm_type = llm_type
        self.parsers = {
            "OpenAILLM": self._parse_openai_llm,
            "GoogleLLM": self._parse_google_llm,
        }

    def parse_args(self, call):
        parser = self.parsers.get(self.llm_type, self._parse_openai_llm)
        return parser(call)

    def _parse_openai_llm(self, call):
        call_args = json.loads(call.function.arguments)
        tool_id = call.function.name.split("_")[-1]
        action_name = call.function.name.rsplit("_", 1)[0]
        return tool_id, action_name, call_args

    def _parse_google_llm(self, call):
        call_args = call.args
        tool_id = call.name.split("_")[-1]
        action_name = call.name.rsplit("_", 1)[0]
        return tool_id, action_name, call_args
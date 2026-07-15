from app.services.llm import llm


class LLMTool:
    """
    Basic tool that sends prompts to the LLM.
    """

    def execute(
    self,
    message: str,
    history=None
    ) -> str:

        return llm.chat(
        prompt=message,
        history=history
        )

llm_tool = LLMTool()
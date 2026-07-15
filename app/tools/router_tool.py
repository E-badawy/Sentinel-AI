import json

from app.services.llm import llm


class RouterTool:
    """
    Uses the LLM to decide which tool should handle a request.
    """

    SYSTEM_PROMPT = """
    You are a routing engine.

    Your job is to choose ONLY ONE tool for the user's request.

    Available tools:

    llm
    - General questions
    - Conversation
    - Explanations
    
    search
    - Internet search
    - Latest news
    - Current events

    analytics
    - Website analytics
    - Portfolio analytics
    - Visitors
    - Countries
    - Traffic
    - Page views
    - Sessions
    - Google Analytics
    - Performance

   email
    - Send emails to external recipients
    - Email a person or organization
    - Requires a recipient email address
    - Example: send this to john@gmail.com
    
    document
    - Summarize uploaded documents
    - Generate PDF or DOCX files
    - Create reports
    - Return generated files
    - Export analysis

    Return ONLY valid JSON.

    Examples:

    User: Latest AI news
    {"tool":"search"}

    User: How many visitors this week?
    {"tool":"analytics"}

    User: Explain tuberculosis
    {"tool":"llm"}

    User: Send an email to John
    {"tool":"email"}
    
    User: Generate a PDF report.
    {"tool":"document"}

    User: Create a DOCX summary.
    {"tool":"document"}

    User: Export this analysis as PDF.
    {"tool":"document"}

    User: Make a report from this document.
    {"tool":"document"}

    User: Email this report to john@gmail.com.
    {"tool":"email"}

    Do not explain your answer.
    Do not use markdown.
    Return valid JSON only.
    """

    def execute(self, message: str) -> str:

        response = llm.chat(
            prompt=message,
            system_prompt=self.SYSTEM_PROMPT
        ).strip()

                
        try:
            return json.loads(response)["tool"].lower()

        except Exception:
            return "llm"


router_tool = RouterTool()
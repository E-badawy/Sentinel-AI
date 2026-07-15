import json

from app.services.llm import llm


class ExtractorService:
    """
    Uses the LLM to extract structured parameters
    from a user's request.
    """

    def extract(
        self,
        message: str,
        schema: str
    ) -> dict:

        system_prompt = f"""
You are an information extraction engine.

Your job is to extract ONLY the requested information.

Return ONLY valid JSON.

Schema:

{schema}

If a field is missing,
return an empty string for that field.

Do not explain.

Do not use markdown.

Return JSON only.
"""

        response = llm.chat(
            prompt=message,
            system_prompt=system_prompt
        ).strip()

        try:
            return json.loads(response)

        except Exception:
            return {}


extractor_service = ExtractorService()
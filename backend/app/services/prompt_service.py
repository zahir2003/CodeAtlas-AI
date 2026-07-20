class PromptService:
    """
    Builds prompts for the LLM.

    The prompt contains:
    - System instructions
    - Previous conversation history
    - Repository context
    - Current user question
    """

    @staticmethod
    def build(
        question: str,
        chunks: list[dict],
        history: list[dict] | None = None,
    ) -> list[dict]:

        history = history or []

        context_parts = []

        for chunk in chunks:
            context_parts.append(f"""File: {chunk['file_path']}

{chunk['code']}
""")

        context = "\n\n".join(context_parts)

        system_prompt = (
            "You are CodeAtlas AI, an expert software engineer.\n"
            "Answer ONLY using the provided repository context.\n"
            "Use the previous conversation if it helps answer follow-up questions.\n"
            "If the answer cannot be found in the context, clearly say so.\n"
            "When appropriate, mention the file where the information comes from."
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        # Previous conversation
        messages.extend(history)

        # Current repository context + question
        messages.append(
            {
                "role": "user",
                "content": f"""
Repository Context:

{context}

Question:
{question}
""",
            }
        )

        return messages

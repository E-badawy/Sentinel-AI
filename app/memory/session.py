from collections import defaultdict


class SessionManager:
    """
    Stores conversations in memory.

    Later this can be replaced by Redis or PostgreSQL
    without changing the agent.
    """

    def __init__(self):
        self.sessions = defaultdict(list)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        self.sessions[session_id].append(
            {
            "role": role,
            "content": content
            }
        )

        # Keep only the most recent 20 messages
        MAX_HISTORY = 20

        if len(self.sessions[session_id]) > MAX_HISTORY:
            self.sessions[session_id] = self.sessions[session_id][-MAX_HISTORY:]
    
    def get_history(self, session_id: str):

                return self.sessions[session_id]

    def clear(self, session_id: str):

        self.sessions[session_id] = []


session_manager = SessionManager()
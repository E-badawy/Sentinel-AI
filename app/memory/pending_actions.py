class PendingActions:

    def __init__(self):

        self.actions = {}

    def set(
        self,
        session_id,
        action
    ):

        self.actions[session_id] = action

    def get(
        self,
        session_id
    ):

        return self.actions.get(session_id)

    def clear(
        self,
        session_id
    ):

        self.actions.pop(
            session_id,
            None
        )


pending_actions = PendingActions()
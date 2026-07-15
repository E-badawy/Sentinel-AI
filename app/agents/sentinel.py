from app.agents.graph import graph

from app.memory.pending_actions import pending_actions

from app.memory.session import session_manager


class SentinelAgent:

   def chat(
    self,
    message: str,
    session_id: str = "default"
    ) -> str:

    # ---------- Pending confirmation ----------

    pending = pending_actions.get(session_id)

    if pending:

        answer = message.strip().lower()

        if answer == "yes":

            pending_actions.clear(session_id)

            response = pending["callback"]()

            session_manager.add_message(
                session_id,
                "assistant",
                response
            )

            return response

        if answer == "no":

            pending_actions.clear(session_id)

            response = "✅ Action cancelled."

            session_manager.add_message(
                session_id,
                "assistant",
                response
            )

            return response

        return "Please reply with YES or NO."

    # ---------- Normal conversation ----------

    history = session_manager.get_history(session_id)

    session_manager.add_message(
        session_id,
        "user",
        message
    )

    result = graph.invoke(
    {
        "session_id": session_id,
        "message": message,
        "response": "",
        "tool": "",
        "history": history
    }
    )
    session_manager.add_message(
        session_id,
        "assistant",
        result["response"]
    )

    if "file" in result:

        return {
        "message": result["response"],
        "file": result["file"]
        }
        
    return result["response"]
        
agent = SentinelAgent()
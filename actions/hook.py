import ORMModels
from ORMModels import request


def after_processed(tracker, action, debug=None):
    sender_id = tracker.current_state()['sender_id']
    if len(sender_id) == 0:
        sender_id = "shell"

    request.Request.create(
        message=tracker.latest_message.get("text"),
        intent=tracker.latest_message['intent'].get('name'),
        sender_id=sender_id,
        response_action=action,
    )


def after_fallback(tracker):
    sender_id = tracker.current_state()['sender_id']
    if len(sender_id) == 0:
        sender_id = "shell"

    request.Request.create(
        message=tracker.latest_message.get("text"),
        sender_id=sender_id,
    )

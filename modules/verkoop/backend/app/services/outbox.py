
# Minimal placeholder for event outbox; extend with retries and delivery to other systems.
from dataclasses import dataclass

@dataclass
class OutboxEvent:
    topic: str
    payload: dict

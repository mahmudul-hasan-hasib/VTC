from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CountingSession:

    video_path: str = ""

    start_time: datetime = field(default_factory=datetime.now)

    incoming: dict = field(default_factory=dict)

    outgoing: dict = field(default_factory=dict)

    notes: str = ""
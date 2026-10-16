from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field

class TicketStatus(StrEnum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"

class Priority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class TicketInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    subject: str = Field(min_length=1, max_length=180)
    description: str = Field(default="", max_length=10000)
    requester: str = Field(min_length=1, max_length=120)
    assignee: str = Field(default="Unassigned", min_length=1, max_length=120)
    status: TicketStatus = TicketStatus.OPEN
    priority: Priority = Priority.MEDIUM

class TicketOutput(TicketInput):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

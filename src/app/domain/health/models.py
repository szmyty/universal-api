from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from .enums import HealthStatus

@dataclass
class HealthCheck:
    """Domain data class representing the health check status."""
    status: HealthStatus
    timestamp: datetime
    details: Dict[str, str]

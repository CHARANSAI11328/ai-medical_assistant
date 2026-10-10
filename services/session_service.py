from typing import List, Dict, Any, Optional
from datetime import datetime

class SessionService:
    """
    Manages user session state, history tracking, and privacy-compliant session resets.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def record_analysis_session(self, image_name: str, specialist_key: str, prediction: Dict[str, Any]):
        entry = {
            "session_id": len(self.history) + 1,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "image_name": image_name,
            "specialist_key": specialist_key,
            "predicted_label": prediction.get("predicted_label"),
            "confidence": prediction.get("confidence", 0.0),
            "is_demo": prediction.get("is_demo", False)
        }
        self.history.append(entry)

    def get_recent_sessions(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self.history[-limit:]

    def clear_session_data(self):
        """Privacy reset: removes all recorded session history."""
        self.history.clear()

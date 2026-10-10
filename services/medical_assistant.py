from typing import Dict, Any, List, Tuple, Optional
from services.gemini_service import GeminiMedicalService
from services.triage_service import TriageService

class MedicalAssistantOrchestrator:
    """
    Orchestrates conversational AI interaction, emergency triage screening, 
    language customization, and session context management.
    """
    def __init__(self):
        self.triage_service = TriageService()
        self.gemini_service = GeminiMedicalService()

    def process_user_message(
        self,
        user_message: str,
        chat_history: List[Dict[str, str]] = None,
        current_prediction: Optional[Dict[str, Any]] = None,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Processes incoming user message through safety triage screening first, 
        then Gemini conversational model if non-emergency.
        """
        # 1. Emergency Triage Screening
        is_emergency, emergency_msg = self.triage_service.evaluate_symptom_urgency(user_message, lang)
        if is_emergency:
            return {
                "response": emergency_msg,
                "is_emergency": True,
                "sources": ["Safety Triage Protocol"],
                "suggested_actions": ["Call Emergency Services", "Seek Immediate Care"]
            }

        # 2. Contextual Prompt Building
        context_str = ""
        if current_prediction:
            context_str = (
                f"\n[Active Image Analysis Context: Specialist={current_prediction.get('specialist_name')}, "
                f"Finding={current_prediction.get('predicted_label')}, Confidence={current_prediction.get('confidence', 0)*100:.1f}%]\n"
            )

        full_prompt = f"{context_str}{user_message}"
        response_text = self.gemini_service.generate_chat_response(full_prompt, chat_history, lang)

        return {
            "response": response_text,
            "is_emergency": False,
            "sources": ["MediScope AI Knowledge Assistant", "Gemini 2.5 Flash"],
            "suggested_actions": ["Ask doctor about this", "Explore model metrics"]
        }

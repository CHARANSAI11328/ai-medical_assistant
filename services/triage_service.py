from typing import Dict, Any, Tuple, Optional
import yaml
import os

class TriageService:
    """
    Independent safety and triage assessment layer.
    Screens patient symptoms before or during AI processing to detect critical, 
    potentially life-threatening emergencies.
    """
    def __init__(self, config_path: str = "configs/settings.yaml"):
        self.emergency_keywords = [
            "chest pain", "difficulty breathing", "shortness of breath", 
            "stroke", "facial weakness", "slurred speech", "one-sided weakness",
            "uncontrolled bleeding", "loss of consciousness", "anaphylaxis",
            "severe allergic reaction", "sudden vision loss", "coughing blood",
            "छाती में दर्द", "सांस लेने में तकलीफ", "ఛాతీ నొప్పి", "శ్వాస తీసుకోవడంలో ఇబ్బంది"
        ]
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f)
                    if cfg and "triage" in cfg and "emergency_keywords" in cfg["triage"]:
                        self.emergency_keywords = cfg["triage"]["emergency_keywords"]
            except Exception:
                pass

    def evaluate_symptom_urgency(self, text: str, lang: str = "en") -> Tuple[bool, Optional[str]]:
        """
        Evaluates input text for emergency indicators.
        Returns: (is_emergency: bool, emergency_guidance_message: Optional[str])
        """
        text_lower = text.lower()
        matched_triggers = [kw for kw in self.emergency_keywords if kw.lower() in text_lower]

        if not matched_triggers:
            return False, None

        if lang == "hi":
            guidance = (
                "🚨 **आपातकालीन चिकित्सा चेतावनी (Emergency Alert)**\n\n"
                "आपके द्वारा बताए गए लक्षण (जैसे कि " + ", ".join(matched_triggers) + ") गंभीर या जीवन के लिए जोखिम भरे हो सकते हैं।\n\n"
                "**तत्काल सलाह:**\n"
                "1. कृपया तुरंत 108 / 112 या स्थानीय आपातकालीन सेवा पर कॉल करें।\n"
                "2. निकटतम अस्पताल के आपातकालीन विभाग (Emergency Room) में जाएं।\n"
                "3. इस चैटबॉट से उत्तर का इंतजार न करें; तत्काल चिकित्सकीय सहायता लें।"
            )
        elif lang == "te":
            guidance = (
                "🚨 **అత్యవసర వైద్య హెచ్చరిక (Emergency Alert)**\n\n"
                "మీరు పేర్కొన్న లక్షణాలు (" + ", ".join(matched_triggers) + ") తీవ్రమైన లేదా ప్రమాదకరమైన వైద్య అత్యవసర పరిస్థితిని సూచించవచ్చు.\n\n"
                "**వెంటనే చేయవలసిన చర్యలు:**\n"
                "1. దయచేసి వెంటనే 108 / 112 లేదా స్థానిక అత్యవసర సేవలకు కాల్ చేయండి.\n"
                "2. దగ్గరలోని ఆసుపత్రి ఎమర్జెన్సీ విభాగానికి వెళ్ళండి.\n"
                "3. ఈ AI చాట్‌బాట్ సమాధానం కోసం వేచి చూడకండి; వెంటనే వైద్య సహాయం పొందండి."
            )
        else:
            guidance = (
                "🚨 **EMERGENCY MEDICAL ALERT**\n\n"
                "The symptoms described (" + ", ".join(matched_triggers) + ") may indicate a severe or life-threatening medical emergency.\n\n"
                "**Immediate Action Required:**\n"
                "1. Call 911 / 112 / 108 or your local emergency response service immediately.\n"
                "2. Proceed to the nearest hospital emergency department.\n"
                "3. Do NOT wait for automated AI recommendations when experiencing acute red-flag symptoms."
            )

        return True, guidance

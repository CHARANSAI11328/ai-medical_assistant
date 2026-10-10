import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv(override=True)

class GeminiMedicalService:
    """
    Service wrapper for Google Gemini API via google-genai, google-generativeai SDK, or HTTP REST.
    Provides structured medical explanations, symptom information, and multilingual guidance.
    """
    def __init__(self, model_name: str = "gemini-3.5-flash", api_key: Optional[str] = None):
        try:
            import streamlit as st
            session_key = st.session_state.get("user_gemini_api_key", None)
        except Exception:
            session_key = None

        self.api_key = api_key or session_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if self.api_key:
            os.environ["GEMINI_API_KEY"] = self.api_key
            os.environ["GOOGLE_API_KEY"] = self.api_key

        self.model_name = model_name
        self.client = None
        self.legacy_model = None
        self.is_available = False
        
        self._initialize_client()

    def _initialize_client(self):
        if not self.api_key:
            logging.warning("GEMINI_API_KEY not found in environment.")
            return

        # Attempt initializing using google-genai SDK first
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
            self.is_available = True
            logging.info(f"Initialized google.genai Client with model {self.model_name}")
            return
        except Exception as e:
            logging.info(f"google.genai SDK initialization note: {e}")

        # Fallback to google.generativeai SDK if available
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=self.api_key)
            self.legacy_model = genai_legacy.GenerativeModel(self.model_name)
            self.is_available = True
            logging.info("Initialized google.generativeai legacy model")
            return
        except Exception as e:
            logging.info(f"SDK initialization note: {e}")

        # Direct REST API capability check
        if self.api_key:
            self.is_available = True

    def generate_prediction_explanation(
        self,
        specialist_name: str,
        modality: str,
        predicted_label: str,
        confidence: float,
        uncertainty_note: str,
        patient_notes: str = "",
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Generates structured plain-language medical educational explanation of model findings.
        Does NOT alter the underlying model prediction.
        """
        if not self.is_available or not self.api_key:
            return self._get_fallback_explanation(specialist_name, predicted_label, confidence, uncertainty_note, lang)

        prompt = f"""
You are a medical AI explanation assistant for MediScope AI (an educational research prototype).
A specialist computer vision model produced the following validated result:

Specialist: {specialist_name}
Modality: {modality}
Predicted Finding: {predicted_label}
Model Confidence: {confidence * 100:.1f}%
Model Uncertainty Note: {uncertainty_note}
Patient Context/Notes: {patient_notes if patient_notes else 'None provided'}
Target Language: {lang}

Generate a clear, compassionate, educational response in JSON format matching this schema:
{{
    "summary": "1-2 sentence plain-language summary of the model finding",
    "plain_meaning": "What this finding means in clear patient-friendly terms",
    "uncertainty_and_limitations": "Important limitations of this AI prediction and why it is not a diagnosis",
    "potential_causes": ["Possible general medical reasons or associations for this finding"],
    "questions_for_doctor": ["3-4 specific questions the patient should ask their doctor"],
    "urgency_guidance": "Recommended timeframe for seeking professional medical review (e.g. routine vs prompt vs immediate)",
    "safety_disclaimer": "Clear medical disclaimer"
}}

IMPORTANT: Return ONLY valid raw JSON. Translate all JSON string values into the target language ({lang}).
"""
        try:
            raw_response = self._call_llm(prompt)
            if "```json" in raw_response:
                raw_response = raw_response.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_response:
                raw_response = raw_response.split("```")[1].split("```")[0].strip()

            parsed = json.loads(raw_response)
            return parsed
        except Exception as e:
            logging.error(f"Error calling Gemini for prediction explanation: {e}")
            return self._get_fallback_explanation(specialist_name, predicted_label, confidence, uncertainty_note, lang)

    def generate_chat_response(self, prompt_text: str, history: list = None, lang: str = "en") -> str:
        """Generates conversational response for general medical information questions."""
        if not self.is_available or not self.api_key:
            return (
                "MediScope AI Medical Assistant (Offline / Demo Mode):\n\n"
                "I am providing general information as the Gemini API key is currently unconfigured or offline.\n"
                "To enable live AI answers, please enter your Gemini API Key in the left sidebar configuration box.\n"
                "For any medical concern, please consult a licensed medical professional."
            )

        system_instruction = (
            "You are MediScope AI, an educational medical assistant. "
            "Respond accurately, empathetically, and clearly. Never diagnose, prescribe medications, or replace a doctor. "
            f"Always reply in language code '{lang}'."
        )

        full_prompt = f"{system_instruction}\n\nUser Question: {prompt_text}"
        try:
            return self._call_llm(full_prompt)
        except Exception as e:
            return f"Error contacting Gemini service: {str(e)}"

    def _call_llm(self, prompt: str) -> str:
        import urllib.request
        import urllib.error
        import time

        # Try direct REST call with gemini-3.5-flash first (fastest and most reliable)
        candidate_models = ["gemini-3.5-flash", self.model_name, "gemini-3.8-flash", "gemini-flash-latest"]
        for model in candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            req = urllib.request.Request(url, data=payload, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=12) as res:
                    data = json.loads(res.read().decode("utf-8"))
                    return data["candidates"][0]["content"]["parts"][0]["text"]
            except urllib.error.HTTPError as err:
                if err.code == 429:
                    logging.warning(f"Rate limited (429) on {model}, backing off briefly...")
                    time.sleep(1)
                else:
                    logging.warning(f"REST call for {model} failed ({err.code}): {err}")
            except Exception as err:
                logging.warning(f"REST call for {model} failed: {err}")

        # Fallback to SDK client if available
        if self.client:
            for model_id in ["gemini-3.5-flash", self.model_name]:
                try:
                    response = self.client.models.generate_content(
                        model=model_id,
                        contents=prompt
                    )
                    return response.text
                except Exception as e:
                    logging.info(f"Client model {model_id} failed: {e}")

        if self.legacy_model:
            try:
                response = self.legacy_model.generate_content(prompt)
                return response.text
            except Exception as e:
                logging.info(f"Legacy model failed: {e}")

        raise RuntimeError("Gemini service rate limited or unavailable.")

    def _get_fallback_explanation(self, specialist: str, label: str, confidence: float, uncertainty: str, lang: str) -> Dict[str, Any]:
        """Provides offline/fallback structured explanation when Gemini is offline."""
        if lang == "hi":
            return {
                "summary": f"{specialist} मॉडल ने '{label}' की संभावना ({confidence*100:.1f}%) जताई है।",
                "plain_meaning": f"यह परिणाम इंगित करता है कि इमेज में {label} से संबंधित विशेषताएं देखी गई हैं।",
                "uncertainty_and_limitations": f"अनिश्चितता नोट: {uncertainty}. यह AI मॉडल एक शोध प्रोटोटाइप है और अंतिम निदान नहीं है।",
                "potential_causes": ["विभिन्न चिकित्सीय या तकनीकी कारण हो सकते हैं।"],
                "questions_for_doctor": [
                    "क्या मुझे इस परिणाम की पुष्टि के लिए विस्तृत जांच की आवश्यकता है?",
                    "इस स्थिति के लिए आगे कौन से नैदानिक परीक्षण अनुशंसित हैं?"
                ],
                "urgency_guidance": "समीक्षा के लिए अपने डॉक्टर या नेत्र/छाती विशेषज्ञ से परामर्श लें।",
                "safety_disclaimer": "MediScope AI केवल शैक्षिक जानकारी प्रदान करता है, चिकित्सीय सलाह नहीं।"
            }
        elif lang == "te":
            return {
                "summary": f"{specialist} మోడల్ '{label}' సంభావ్యతను ({confidence*100:.1f}%) గుర్తించింది.",
                "plain_meaning": f"ఈ ఫలితం చిత్రంలో {label} కి సంబంధించిన లక్షణాలను సూచిస్తుంది.",
                "uncertainty_and_limitations": f"అనిశ్చితి గమనిక: {uncertainty}. ఈ AI పరిశోధన ప్రోటోటైప్ మాత్రమే.",
                "potential_causes": ["వివిధ వైద్య లేదా సాంకేతిక కారణాలు ఉండవచ్చు."],
                "questions_for_doctor": [
                    "ఈ ఫలితాన్ని నిర్ధారించడానికి నాకు తదుపరి పరీక్షలు అవసరమా?",
                    "ముందు జాగ్రత్తగా ఏ చర్యలు తీసుకోవాలి?"
                ],
                "urgency_guidance": "సరైన వైద్య సలహా కోసం మీ వైద్యుడిని సంప్రదించండి.",
                "safety_disclaimer": "MediScope AI విద్యా విషయక సమాచారాన్ని మాత్రమే అందిస్తుంది."
            }
        else:
            return {
                "summary": f"{specialist} model identified potential signs of '{label}' ({confidence*100:.1f}% confidence).",
                "plain_meaning": f"This finding indicates visual patterns consistent with {label} in the uploaded scan.",
                "uncertainty_and_limitations": f"Uncertainty: {uncertainty}. Model predictions require expert clinical verification.",
                "potential_causes": ["Requires professional clinical correlation and evaluation."],
                "questions_for_doctor": [
                    "Does this scan finding match my clinical history?",
                    "What confirmatory diagnostic tests are recommended?",
                    "What preventative or therapeutic steps should be discussed?"
                ],
                "urgency_guidance": "Schedule a follow-up review with a qualified healthcare provider.",
                "safety_disclaimer": "MediScope AI provides research and educational assistance, NOT a medical diagnosis."
            }

from services.triage_service import TriageService

def test_triage_emergency_detection_english():
    triage = TriageService()
    is_emergency, msg = triage.evaluate_symptom_urgency("I am experiencing severe chest pain and difficulty breathing")
    assert is_emergency is True
    assert "EMERGENCY MEDICAL ALERT" in msg

def test_triage_non_emergency():
    triage = TriageService()
    is_emergency, msg = triage.evaluate_symptom_urgency("What is diabetic retinopathy?")
    assert is_emergency is False
    assert msg is None

def test_triage_multilingual_hindi():
    triage = TriageService()
    is_emergency, msg = triage.evaluate_symptom_urgency("मुझे छाती में दर्द हो रहा है", lang="hi")
    assert is_emergency is True
    assert "आपातकालीन चिकित्सा चेतावनी" in msg

def test_triage_multilingual_telugu():
    triage = TriageService()
    is_emergency, msg = triage.evaluate_symptom_urgency("నాకు ఛాతీ నొప్పి వస్తోంది", lang="te")
    assert is_emergency is True
    assert "అత్యవసర వైద్య హెచ్చరిక" in msg

if __name__ == "__main__":
    test_triage_emergency_detection_english()
    test_triage_non_emergency()
    test_triage_multilingual_hindi()
    test_triage_multilingual_telugu()
    print("All Triage Service Unit Tests Passed!")

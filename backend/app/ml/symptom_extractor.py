import re

CANONICAL_SYMPTOMS = {
    "fever": [
        "fever",
        "high temp",
        "temperature",
        "chills",
        "febrile",
        "hot",
        "sweating",
        "shivering",
    ],
    "chest_pain": [
        "chest pain",
        "chest tightness",
        "chest pressure",
        "heart pain",
        "crushing chest",
        "sternum pain",
        "angina",
    ],
    "shortness_of_breath": [
        "short of breath",
        "shortness of breath",
        "breathless",
        "breathing difficulty",
        "dyspnea",
        "wheezing",
        "gasping",
        "hard to breathe",
    ],
    "cough": ["cough", "dry cough", "productive cough", "hacking", "phlegm", "mucus", "coughing"],
    "headache": [
        "headache",
        "migraine",
        "head throbbing",
        "pain in head",
        "temple pain",
        "cranial pressure",
    ],
    "fatigue": ["fatigue", "tired", "exhausted", "lethargic", "weakness", "low energy", "worn out"],
    "sore_throat": [
        "sore throat",
        "throat pain",
        "throat irritation",
        "difficulty swallowing",
        "scratchy throat",
    ],
    "nausea_vomiting": ["nausea", "nauseous", "vomiting", "threw up", "throwing up", "queasy"],
    "abdominal_pain": [
        "abdominal pain",
        "stomach pain",
        "belly ache",
        "cramps",
        "gut pain",
        "stomach cramps",
    ],
    "dizziness": ["dizzy", "dizziness", "lightheaded", "vertigo", "spinning sensation", "unsteady"],
    "body_aches": [
        "body aches",
        "muscle pain",
        "joint pain",
        "myalgia",
        "arthralgia",
        "sore muscles",
    ],
    "diarrhea": ["diarrhea", "loose stool", "watery stool", "frequent bowel movements"],
    "rash": ["rash", "skin hives", "red bumps", "itching skin", "dermatitis", "spots"],
    "palpitations": [
        "palpitations",
        "racing heart",
        "rapid heartbeat",
        "fluttering heart",
        "tachycardia",
    ],
    "stiff_neck": ["stiff neck", "neck stiffness", "cannot bend neck", "nuchal rigidity"],
}


def extract_symptoms(text: str) -> list[str]:
    """
    NLP symptom extractor that normalizes natural language text
    and returns canonical clinical symptom tokens.
    """
    clean_text = text.lower()
    matched_symptoms: set[str] = set()

    for canonical, synonyms in CANONICAL_SYMPTOMS.items():
        for syn in synonyms:
            pattern = r"\b" + re.escape(syn) + r"\b"
            if re.search(pattern, clean_text):
                matched_symptoms.add(canonical)
                break

    # If no specific synonym matched, extract keyword fallback
    if not matched_symptoms:
        words = re.findall(r"\w+", clean_text)
        for w in words:
            if w in CANONICAL_SYMPTOMS:
                matched_symptoms.add(w)

    return sorted(list(matched_symptoms))

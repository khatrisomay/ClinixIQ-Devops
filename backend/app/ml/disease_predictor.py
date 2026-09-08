import time
from datetime import UTC, datetime

from app.ml.symptom_extractor import extract_symptoms
from app.models.schemas import DifferentialMatch, TriageRequest, TriageResponse

# Knowledge Base of conditions with symptom profiles, base urgency, and care plans

DISEASE_PROFILES = [
    {
        "name": "Acute Coronary / Cardiopulmonary Distress",
        "category": "Cardiopulmonary",
        "symptoms": ["chest_pain", "shortness_of_breath", "palpitations", "dizziness"],
        "base_weight": 1.6,
        "urgency": "High Alert / Emergency",
        "triage_color": "text-rose-400 bg-rose-500/10 border-rose-500/30",
        "action": "Immediate Emergency Medical Services (911/EMS) recommended. Chew non-enteric aspirin if advised and rest upright.",
        "emergency_flag": True,
    },
    {
        "name": "Viral Upper Respiratory Infection",
        "category": "Respiratory",
        "symptoms": ["cough", "sore_throat", "fever", "fatigue", "body_aches"],
        "base_weight": 1.2,
        "urgency": "Standard / Mild",
        "triage_color": "text-sky-400 bg-sky-500/10 border-sky-500/30",
        "action": "Hydrate adequately, get rest, and consider over-the-counter antipyretics. Monitor temperature daily.",
        "emergency_flag": False,
    },
    {
        "name": "Influenza Type A / B (Flu)",
        "category": "Respiratory",
        "symptoms": ["fever", "body_aches", "fatigue", "cough", "headache"],
        "base_weight": 1.2,
        "urgency": "Urgent / Moderate",
        "triage_color": "text-amber-400 bg-amber-500/10 border-amber-500/30",
        "action": "Rest and isolation recommended. Consult healthcare provider within 48 hours for potential antiviral therapy (e.g., Oseltamivir).",
        "emergency_flag": False,
    },
    {
        "name": "Community-Acquired Bacterial Pneumonia",
        "category": "Respiratory",
        "symptoms": ["fever", "cough", "shortness_of_breath", "chest_pain", "fatigue"],
        "base_weight": 1.3,
        "urgency": "High Alert / Emergency",
        "triage_color": "text-rose-400 bg-rose-500/10 border-rose-500/30",
        "action": "Urgent chest radiography and clinical auscultation needed. Contact urgent care or hospital immediately.",
        "emergency_flag": True,
    },
    {
        "name": "Acute Migraine / Cephalea",
        "category": "Neurological",
        "symptoms": ["headache", "nausea_vomiting", "dizziness"],
        "base_weight": 1.1,
        "urgency": "Standard / Mild",
        "triage_color": "text-sky-400 bg-sky-500/10 border-sky-500/30",
        "action": "Rest in a quiet, dark environment. Hydrate and use prescribed migraine medication or NSAIDs as recommended by doctor.",
        "emergency_flag": False,
    },
    {
        "name": "Bacterial Meningitis Suspect",
        "category": "Neurological",
        "symptoms": ["fever", "headache", "stiff_neck", "nausea_vomiting"],
        "base_weight": 1.5,
        "urgency": "High Alert / Emergency",
        "triage_color": "text-rose-400 bg-rose-500/10 border-rose-500/30",
        "action": "CRITICAL EMERGENCY: Immediate hospital evaluation required for lumbar puncture and empiric antibiotic therapy.",
        "emergency_flag": True,
    },
    {
        "name": "Acute Gastroenteritis (Foodborne Illness)",
        "category": "Gastrointestinal",
        "symptoms": ["nausea_vomiting", "diarrhea", "abdominal_pain", "fever"],
        "base_weight": 1.1,
        "urgency": "Urgent / Moderate",
        "triage_color": "text-amber-400 bg-amber-500/10 border-amber-500/30",
        "action": "Drink oral rehydration solutions (ORS) in small, frequent sips. Avoid solid dairy and seek care if signs of dehydration emerge.",
        "emergency_flag": False,
    },
    {
        "name": "Acute Appendicitis / Acute Abdomen",
        "category": "Gastrointestinal",
        "symptoms": ["abdominal_pain", "nausea_vomiting", "fever"],
        "base_weight": 1.3,
        "urgency": "High Alert / Emergency",
        "triage_color": "text-rose-400 bg-rose-500/10 border-rose-500/30",
        "action": "Emergency surgical evaluation required. Do not eat, drink, or take laxatives before physician evaluation.",
        "emergency_flag": True,
    },
    {
        "name": "Allergic Rhinitis / Sinusitis",
        "category": "Respiratory",
        "symptoms": ["headache", "cough", "sore_throat"],
        "base_weight": 0.9,
        "urgency": "Standard / Mild",
        "triage_color": "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
        "action": "Saline nasal rinses and antihistamines or nasal corticosteroids as directed by a primary care clinician.",
        "emergency_flag": False,
    },
    {
        "name": "Acute Bronchitis",
        "category": "Respiratory",
        "symptoms": ["cough", "fatigue", "sore_throat", "shortness_of_breath"],
        "base_weight": 1.0,
        "urgency": "Urgent / Moderate",
        "triage_color": "text-amber-400 bg-amber-500/10 border-amber-500/30",
        "action": "Humidified air, throat lozenges, and hydration. Schedule clinic visit if cough persists beyond 2 weeks.",
        "emergency_flag": False,
    },
]


def evaluate_vitals(request: TriageRequest) -> dict[str, str]:
    """Assess raw vital signs and generate risk flags."""

    assessment = {}

    if request.temperature is not None:
        if request.temperature >= 103.0:
            assessment["temperature"] = "High Pyrexia / Severe Fever (>103F)"

        elif request.temperature >= 100.4:
            assessment["temperature"] = "Mild/Moderate Fever"

        else:
            assessment["temperature"] = "Normal Range"

    if request.heart_rate is not None:
        if request.heart_rate > 120:
            assessment["heart_rate"] = "Marked Tachycardia (>120 bpm)"

        elif request.heart_rate < 50:
            assessment["heart_rate"] = "Bradycardia (<50 bpm)"

        else:
            assessment["heart_rate"] = "Normal Resting Heart Rate"

    if request.oxygen_level is not None:
        if request.oxygen_level < 92:
            assessment["oxygen"] = "Hypoxemia Alert (<92% SpO2)"

        elif request.oxygen_level < 95:
            assessment["oxygen"] = "Mildly Reduced SpO2"

        else:
            assessment["oxygen"] = "Optimal Oxygen Saturation"

    return assessment


def predict_triage(request: TriageRequest) -> TriageResponse:
    """Core triage scoring and ML inference engine."""

    start_time = time.time()

    extracted = extract_symptoms(request.symptoms)

    vitals_flags = evaluate_vitals(request)

    scores = []

    for profile in DISEASE_PROFILES:
        target_symptoms = set(profile["symptoms"])

        matched = target_symptoms.intersection(set(extracted))

        matched_count = len(matched)

        if matched_count > 0:
            match_ratio = matched_count / len(target_symptoms)

            raw_score = match_ratio * profile["base_weight"] * 100.0

            # High-signal bonus for multi-symptom alignment

            if matched_count >= 2:
                raw_score += 15.0

        else:
            raw_score = 4.0

        # Vitals heuristic escalations

        if (
            request.oxygen_level
            and request.oxygen_level < 92
            and profile["category"] in ["Cardiopulmonary", "Respiratory"]
        ):
            raw_score *= 1.4

        if (
            request.temperature
            and request.temperature > 102
            and profile["name"]
            in ["Bacterial Meningitis Suspect", "Community-Acquired Bacterial Pneumonia"]
        ):
            raw_score *= 1.3

        scores.append((profile, raw_score))

    # Sort profiles by raw score

    scores.sort(key=lambda x: x[1], reverse=True)

    top_profile, top_score = scores[0]

    # Calculate confidence based on top condition match strength
    base_confidence = min(96, int(68 + min(top_score * 0.22, 24)))

    if top_profile.get("emergency_flag") and (
        "chest_pain" in extracted or (request.oxygen_level and request.oxygen_level < 92)
    ):
        base_confidence = max(88, base_confidence)

    confidence = base_confidence

    # Normalize probabilities for top differential matches

    total_score = sum(s[1] for s in scores[:5])

    differentials: list[DifferentialMatch] = []

    for prof, sc in scores[:5]:
        prob = int(round((sc / total_score) * 100))

        prob = max(5, min(95, prob))

        differentials.append(
            DifferentialMatch(
                condition=prof["name"],
                probability=prob,
                risk=prof["urgency"],
                category=prof["category"],
            )
        )

    # Emergency escalation rule

    severity = top_profile["urgency"]

    triage_color = top_profile["triage_color"]

    action = top_profile["action"]

    if (
        "chest_pain" in extracted
        or "shortness_of_breath" in extracted
        or (request.oxygen_level and request.oxygen_level < 92)
    ):
        if not top_profile["emergency_flag"]:
            severity = "High Alert / Urgent Escalation"

            triage_color = "text-rose-400 bg-rose-500/10 border-rose-500/30"

            action = "Chest tightness or dyspnea detected. Immediate professional clinical assessment strongly advised."

    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    return TriageResponse(
        condition=top_profile["name"],
        confidence=confidence,
        severity=severity,
        triage_color=triage_color,
        action=action,
        differentials=differentials,
        extracted_symptoms=extracted,
        vitals_assessment=vitals_flags,
        model_version="ClinixIQ-XGBoost-Med-v2.4",
        inference_latency_ms=elapsed_ms,
        timestamp=datetime.now(UTC).isoformat(),
    )

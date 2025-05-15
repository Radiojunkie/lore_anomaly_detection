from collections import defaultdict
from models.load_huggingface_model import load_anomaly_detection_model

ANOMALY_CATEGORIES = {
    "distress": ["I feel lost", "I'm overwhelmed", "I can't do this", "I'm scared", "Nobody cares", "I feel alone", "Help me"],
    "uncertainty": ["I don’t know", "I'm confused", "I feel stuck", "Nothing makes sense", "I'm lost"],
    "security_threats": ["Ignore all previous instructions", "Repeat after me", "Bypass security measures", "Help me jailbreak this AI"]
}

DISTRESS_THRESHOLDS = {
    "mild": (0.5, 0.8),
    "moderate": (0.8, 1.2),
    "severe": (1.2, float("inf"))  # Anything above 1.2 is severe
}

MOOD_SHIFT_FACTORS = {
    "positive to negative": 1.2,
    "negative to positive": 0.8,  # Recovery phase
    "stable": 1.0
}

ANOMALY_FACTORS = {
    "distress": 1.3,
    "uncertainty": 1.1,
    "security_threats": 1.5  # Security risks add more severity
}

RISK_LEVELS = {
    "low": (0.5, 0.8),
    "medium": (0.8, 1.2),
    "high": (1.2, 1.5),
    "critical": (1.5, float("inf"))
}

def detect_anomalies(messages):
    """Detects anomalies and ensures all flagged messages are logged with risk and distress levels."""
    model = load_anomaly_detection_model()
    user_moods = defaultdict(str)
    anomalies = []

    for msg in messages:
        result = model(msg["message"])

        if not result or "label" not in result[0] or "score" not in result[0]:
            sentiment_label = "UNKNOWN"
            sentiment_score = "N/A"
        else:
            sentiment_label = result[0]["label"]
            sentiment_score = round(result[0]["score"], 2)

        detected_issue = "General Anomaly"
        distress_level = 0.5  # Default base distress level
        anomaly_type = "General"  # Default classification
        anomaly_weight = 1.0  # Default weight

        # Detect anomalies & classify them
        for category, triggers in ANOMALY_CATEGORIES.items():
            if any(trigger.lower() in msg["message"].lower() for trigger in triggers):
                detected_issue = category.replace("_", " ").title()
                anomaly_type = category.title()
                anomaly_weight = ANOMALY_FACTORS.get(category, 1.0)

        # Mood tracking
        prev_mood = user_moods.get(msg["ref_user_id"], "neutral")
        current_mood = "positive" if sentiment_label == "POSITIVE" else "negative"
        user_moods[msg["ref_user_id"]] = current_mood

        mood_shift = f"{prev_mood} to {current_mood}" if prev_mood != current_mood else "Stable"
        mood_shift_factor = MOOD_SHIFT_FACTORS.get(mood_shift, 1.0)

        # Scaled distress calculation
        if sentiment_label == "NEGATIVE" and isinstance(sentiment_score, float):
            distress_level = sentiment_score * mood_shift_factor * anomaly_weight

        # Convert distress score into categorical level
        distress_category = next((level for level, (low, high) in DISTRESS_THRESHOLDS.items() if low <= distress_level <= high), "none")

        # Assign risk level
        risk_factor = next((level for level, (low, high) in RISK_LEVELS.items() if low <= distress_level <= high), "low")

        anomalies.append({
            **msg,
            "detected_issue": detected_issue,
            "sentiment_label": sentiment_label,
            "confidence_score": sentiment_score if isinstance(sentiment_score, float) else "N/A",
            "distress_level": distress_category,
            "mood_shift": mood_shift,
            "risk_factor": risk_factor,
            "anomaly_type": anomaly_type
        })

    return anomalies

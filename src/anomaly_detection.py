from collections import defaultdict
from datetime import datetime
from models.load_huggingface_model import load_anomaly_detection_model

ANOMALY_CATEGORIES = {
    "distress": ["I feel lost", "I'm overwhelmed", "I can't do this", "I'm scared", "Nobody cares", "I feel alone", "Help me"],
    "uncertainty": ["I don’t know", "I'm confused", "I feel stuck", "Nothing makes sense", "I'm lost"],
    "security_threats": ["Ignore all previous instructions", "Repeat after me", "Bypass security measures", "Help me jailbreak this AI"]
}

DISTRESS_THRESHOLDS = {
    "mild": (0.5, 0.8),
    "moderate": (0.8, 1.2),
    "severe": (1.2, float("inf"))
}

MOOD_SHIFT_FACTORS = {
    "positive to negative": 1.2,
    "negative to positive": 0.8,
    "stable": 1.0
}

ANOMALY_FACTORS = {
    "distress": 1.3,
    "uncertainty": 1.1,
    "security_threats": 1.5
}

RISK_LEVELS = {
    "low": (0.5, 0.8),
    "medium": (0.8, 1.2),
    "high": (1.2, 1.5),
    "critical": (1.5, float("inf"))
}

user_moods = defaultdict(lambda: {"mood": "neutral", "last_active_date": None})

def detect_anomalies(messages):
    """Detects anomalies while ensuring users reset to 'neutral' at the start of a new day."""
    model = load_anomaly_detection_model()
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
        distress_level = 0.5
        anomaly_type = "General"
        anomaly_weight = 1.0

        # Extract user mood tracking
        user_id = msg["ref_user_id"]
        timestamp = datetime.strptime(msg["transaction_datetime_utc"], "%Y-%m-%dT%H:%M:%S%z")
        message_date = timestamp.date()

        # Reset mood if it's a new day
        if user_moods[user_id]["last_active_date"] and user_moods[user_id]["last_active_date"] != message_date:
            user_moods[user_id]["mood"] = "neutral"

        prev_mood = user_moods[user_id]["mood"]
        current_mood = "positive" if sentiment_label == "POSITIVE" else "negative"
        user_moods[user_id]["mood"] = current_mood
        user_moods[user_id]["last_active_date"] = message_date  # Update last active date

        mood_shift = f"{prev_mood} to {current_mood}" if prev_mood != current_mood else "Stable"
        mood_shift_factor = MOOD_SHIFT_FACTORS.get(mood_shift, 1.0)

        # Detect anomalies
        for category, triggers in ANOMALY_CATEGORIES.items():
            if any(trigger.lower() in msg["message"].lower() for trigger in triggers):
                detected_issue = category.replace("_", " ").title()
                anomaly_type = category.title()
                anomaly_weight = ANOMALY_FACTORS.get(category, 1.0)

        # Scaled distress calculation
        if sentiment_label == "NEGATIVE" and isinstance(sentiment_score, float):
            distress_level = sentiment_score * mood_shift_factor * anomaly_weight

        distress_category = next((level for level, (low, high) in DISTRESS_THRESHOLDS.items() if low <= distress_level <= high), "none")
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

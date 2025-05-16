import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), "logs")
log_file = os.path.join(log_dir, "high_risk_anomalies.log")

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=log_file,
    level=logging.WARNING,
    format="%(asctime)s - Anomaly Detection - %(message)s"
)

processed_conversations = set()
CACHE_RESET_INTERVAL = 10000  # Reset cache every 10000 messages

def format_alert_message(anomalous_message):
    """Formats detected anomaly alert with sentiment label, confidence score, and mood shifts."""
    return (
        f"🚨 *User Alert!*\n"
        f"👤 *User:* {anomalous_message['screen_name']}\n"
        f"🗣️ *Message:* \"{anomalous_message['message']}\"\n"
        f"📌 *Conversation ID:* {anomalous_message['ref_conversation_id']}\n"
        f"🆔 *User ID:* {anomalous_message['ref_user_id']}\n"
        f"⏰ *Timestamp:* {anomalous_message['transaction_datetime_utc']}\n"
        f"⚠️ *Sentiment Label:* {anomalous_message.get('sentiment_label', 'UNKNOWN')}\n"
        f"📊 *Confidence Score:* {anomalous_message.get('confidence_score', 'N/A')}\n"
        f"🔄 *Mood Shift:* {anomalous_message.get('mood_shift', 'None')}\n"
        f"🔥 *Distress Level:* {anomalous_message.get('distress_level', 'None')}\n"
        f"🔥 *Potential Concern:* {anomalous_message.get('potential_concern', 'None')}\n"
    )

def send_alert(anomalous_messages):
    """Logs high-risk anomalies, prevents duplicate alerts, and clears cache periodically."""
    global processed_conversations

    if len(processed_conversations) > CACHE_RESET_INTERVAL:
        print("♻️ Clearing cache to prevent memory overload...")
        processed_conversations.clear()

    for msg in anomalous_messages:
        conversation_id = msg.get("ref_conversation_id")

        if not conversation_id:
            print(f"⚠️ Skipping alert due to missing ref_conversation_id: {msg}")
            continue

        if conversation_id in processed_conversations:
            continue

        processed_conversations.add(conversation_id)

        readable_alert = format_alert_message(msg)
        logging.warning(readable_alert)

        # Simulated Slack output
        print("\n--- Simulated Slack Alert ---")
        print(readable_alert)
        print("----------------------------")

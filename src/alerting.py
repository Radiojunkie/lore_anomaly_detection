import logging
import os
from collections import defaultdict

log_dir = os.path.join(os.path.dirname(__file__), "logs")
log_file = os.path.join(log_dir, "high_risk_anomalies.log")

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=log_file,
    level=logging.WARNING,
    format="%(asctime)s - Anomaly Detection - %(message)s"
)

processed_messages = set()
CACHE_RESET_INTERVAL = 10000  # Reset cache every 10,000 messages

def format_alert_message(anomalous_message):
    """Formats instant alert messages, filtering out StoryBot."""
    if anomalous_message["screen_name"] == "StoryBot":
        return None  # ❌ Skip StoryBot alerts

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
        f"🔥 *Risk Factor:* {anomalous_message.get('risk_factor', 'None')}\n"
        f"🛑 *Anomaly Type:* {anomalous_message.get('anomaly_type', 'None')}\n"
    )

def format_log_entry(conversation_messages):
    """Formats logged conversations grouped by ref_conversation_id, sorted by timestamp."""
    log_entry = "\n📌 **Conversation Log** 📌\n"

    for msg in sorted(conversation_messages, key=lambda x: x["transaction_datetime_utc"]):
        log_entry += (
            f"⏰ {msg['transaction_datetime_utc']} | 🗣 {msg['screen_name']}: {msg['message']}\n"
        )

    log_entry += "\n---------------------------------\n"
    return log_entry

def send_alert(anomalous_messages):
    """Logs high-risk anomalies instantly (excluding StoryBot) & stores full conversation history."""
    global processed_messages

    if len(processed_messages) > CACHE_RESET_INTERVAL:
        print("♻️ Clearing cache to prevent memory overload...")
        processed_messages.clear()

    conversation_groups = defaultdict(list)

    for msg in anomalous_messages:
        message_id = msg.get("transaction_datetime_utc") + str(msg.get("ref_user_id"))

        if not message_id:
            print(f"⚠️ Skipping alert due to missing unique message ID: {msg}")
            continue

        if message_id in processed_messages:
            continue  # ✅ Prevent duplicate alerts

        processed_messages.add(message_id)

        # ✅ **Instant Alert (excluding StoryBot)**
        readable_alert = format_alert_message(msg)
        if readable_alert:
            logging.warning(readable_alert)
            print("\n--- Simulated Slack Alert ---")
            print(readable_alert)
            print("----------------------------")

        # ✅ **Group messages for logging based on conversation ID**
        conversation_groups[msg["ref_conversation_id"]].append(msg)

    # ✅ **Log entire conversations grouped by ID, maintaining timestamp order**
    for conversation_id, messages in conversation_groups.items():
        formatted_log = format_log_entry(messages)
        logging.warning(formatted_log)

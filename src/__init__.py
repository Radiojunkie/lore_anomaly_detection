import time
from kafka_stream import load_conversation_data
from anomaly_detection import detect_anomalies
from alerting import send_alert

DATA_PATH = "data/conversations.json"
POLL_INTERVAL = 3  # Check for new messages every 3 seconds

def monitor_conversation_stream():
    """Continuously monitors and analyzes conversation data for anomalies."""
    print("🔍 Monitoring conversation stream for high-risk anomalies...")

    while True:
        try:
            conversations = load_conversation_data(DATA_PATH)
            messages = [msg for conv in conversations for msg in conv["messages_list"]]

            anomalies = detect_anomalies(messages)

            if anomalies:
                send_alert(anomalies)

            time.sleep(POLL_INTERVAL)

        except Exception as e:
            print(f"Error encountered: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    monitor_conversation_stream()

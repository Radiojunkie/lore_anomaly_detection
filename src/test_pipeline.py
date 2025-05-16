import time
from datetime import datetime, timezone
from anomaly_detection import detect_anomalies

def live_simulation():
    """Simulates real-time anomaly detection where users input messages."""
    print("🔍 Live Anomaly Detection Simulation")
    print("Type a message and press Enter to analyze it. Type 'exit' to quit.")

    while True:
        user_input = input("\nEnter a message: ")

        if user_input.lower() == "exit":
            print("🔻 Simulation Stopped")
            break

        # ✅ Ensure required fields exist in test data
        test_message = [{
            "message": user_input,
            "screen_name": "TestUser",  # Simulating a user
            "ref_user_id": "12345",  # Simulating a user ID
            "ref_conversation_id": "67890",  # Simulating a conversation ID
            "transaction_datetime_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        }]

        anomalies = detect_anomalies(test_message)

        if anomalies and anomalies[0].get("sentiment_label"):
            sentiment = anomalies[0]["sentiment_label"]
            if sentiment == "NEGATIVE":
                print("😢 **Sad Message Detected!**")
            elif sentiment == "POSITIVE":
                print("😊 **Happy Message Detected!**")
            else:
                print("😐 **Neutral Message Detected!**")

            print(anomalies[0])  # Show full anomaly details for debugging
        else:
            print("✅ Message appears normal.")

        time.sleep(1)  # Simulates real-time processing delay


if __name__ == "__main__":
    live_simulation()

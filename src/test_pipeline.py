import time
from anomaly_detection import detect_high_risk_anomalies


def live_simulation():
    """Simulates real-time anomaly detection where users input messages."""
    print("🔍 Live Anomaly Detection Simulation")
    print("Type a message and press Enter to analyze it. Type 'exit' to quit.")

    while True:
        user_input = input("\nEnter a message: ")

        if user_input.lower() == "exit":
            print("🔻 Simulation Stopped")
            break

        test_message = [{"message": user_input}]
        anomalies = detect_high_risk_anomalies(test_message)

        if anomalies:
            print("🚨 High-Risk Message Detected!")
        else:
            print("✅ Message appears normal.")

        time.sleep(1)  # Simulates real-time processing delay


if __name__ == "__main__":
    live_simulation()

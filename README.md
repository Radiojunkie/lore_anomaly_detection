## How It Works
# 1. Data Ingestion (kafka_stream.py)

    Mimics a Kafka-style stream by reading new messages from conversations.json.


# 2. Anomaly Detection (anomaly_detection.py)

    Flags high-risk messages based on sentiment scores and key phrases (e.g., "I feel lost", "I'm overwhelmed").

    Uses a pretrained Hugging Face model to assess emotions in conversations.

# 3. Logging & Alerting (alerting.py)

    Stores anomalies in logs/anomalies.log for further review.

    Prints high-risk messages immediately for intervention.

# Real-Time Conversational Anomaly Detection

## Installation
Run the following command to install all required dependencies:
```bash
pip install -r requirements.txt
```
## Download and Save the Pretrained Model
```bash
python models/load_huggingface_model.py
```
## Running the Streaming Pipeline
```commandline
python src/__init__.py
```
## Running the Streaming Pipeline Alternate
```
If the cmd doesnt work please go to the __init__.py and run it from there.
```
## Running Tests(To see how it would work with input)
```commandline
python src/test_pipeline.py
```

# 🔎 Understanding the Anomaly Detection Output

## System analyzes messages using sentiment analysis, mood shifts, and distress scaling to detect emotional distress and high-risk anomalies. Each alert includes the following fields:
Field Name	Description

⚠️ Sentiment Label	Indicates whether the message expresses POSITIVE, NEGATIVE, or NEUTRAL emotions based on machine learning analysis.

📊 Confidence Score	A 0 to 1 score representing how strongly the sentiment model classifies the message as positive or negative.

🔄 Mood Shift	Detects emotional changes from previous messages, tracking shifts such as "neutral to negative" or "positive to negative".

🔥 Distress Level	A scaled rating (mild, moderate, severe) based on sentiment confidence, mood shifts, and anomaly factors.

🚨 Potential Concern	Classifies whether the detected anomaly is related to distress, security risks, uncertainty, or general concerns.

📌 How Each Field Works

⚠️ Sentiment Label

## The sentiment model classifies a message as:

    POSITIVE → The message contains optimism, happiness, or enthusiasm.

    NEGATIVE → The message conveys sadness, frustration, distress, or concern.

    NEUTRAL → The message doesn't strongly lean toward positive or negative.

📊 Confidence Score

    Range: 0 to 1

    Closer to 1.0 → The model is very confident in its classification.

    Closer to 0.5 → The sentiment is ambiguous, meaning it could be neutral or unclear.

🔄 Mood Shift

Mood shifts track changes in a user’s emotional state between consecutive messages. Possible values:

    "positive to negative" → User was optimistic but now expresses distress.

    "negative to positive" → User seems to be recovering emotionally.

    "stable" → No significant mood change from the last message.

🔥 Distress Level (Mathematically Derived)

Distress level is not a simple negative sentiment flag—it's scaled based on multiple factors: Formula: Distress Level = Sentiment Score × Mood Shift Factor × Anomaly Factor

    Sentiment Score: Higher confidence in negative sentiment → Higher distress

    Mood Shift Factor:

        "positive to negative" → Boost distress by 1.2

        "stable" → No effect

    Anomaly Factor:

        "I feel lost" → Boost distress by 1.3

        "I don’t know" → Boost distress by 1.1

Thresholds for Classification
Distress Score	Classification
0.5 - 0.8	None/Mild
0.8 - 1.2	Moderate
1.2+	Severe
🚨 Potential Concern

This field summarizes the nature of the anomaly, categorizing messages into:

    Distress → The message expresses strong emotional distress.

    Security Threat → The user attempts to bypass security or manipulate the AI.

    Uncertainty → The message shows confusion, doubt, or lack of direction.

    General Concern → The message isn’t high-risk but requires monitoring.

🚀 Example Breakdown
Message: "I don't know what to do anymore. I'm completely lost."
Field	Value	Reasoning

⚠️ Sentiment Label	NEGATIVE	The model detects high confidence in distress.

📊 Confidence Score	0.92	The sentiment model is highly certain this message expresses negative emotions.

🔄 Mood Shift	"positive to negative"	The user was previously optimistic but now expresses uncertainty.

🔥 Distress Level	"severe"	Computed as 0.92 × 1.2 × 1.3 = 1.43 (Severe range).

🚨 Potential Concern	"Distress"	The message contains distress-related keywords like "lost" and "don't know."


This system ensures alerts are scalable, context-aware, and not falsely flagging neutral messages. Every detected anomaly includes detailed reasoning behind its classification.


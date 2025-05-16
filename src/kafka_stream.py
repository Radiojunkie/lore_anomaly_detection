import json

def load_conversation_data(file_path):
    """Reads conversations from a Kafka-style stream and filters out messages from StoryBot."""
    with open(file_path, 'r') as file:
        conversations = json.load(file)

    return conversations

# import json
# from kafka import KafkaConsumer
#
# KAFKA_TOPIC = "conversation_stream"
# KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # Update with actual Kafka server
#
# def load_conversation_data():
#     """Consumes messages from a Kafka stream without filtering, allowing full conversations to be processed."""
#     consumer = KafkaConsumer(
#         KAFKA_TOPIC,
#         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#         value_deserializer=lambda msg: json.loads(msg.decode('utf-8'))
#     )
#
#     conversations = []
#
#     for message in consumer:
#         conversation = message.value
#         conversations.append(conversation)  # ✅ No filtering, stores full messages
#         print(f"Received conversation: {conversation}")
#
#     return conversations


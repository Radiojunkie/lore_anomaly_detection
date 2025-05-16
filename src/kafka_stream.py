import json

def load_conversation_data(file_path):
    """Reads conversations from a Kafka-style stream and filters out messages from StoryBot."""
    with open(file_path, 'r') as file:
        conversations = json.load(file)

    # Remove StoryBot messages from each conversation
    for conversation in conversations:
        conversation["messages_list"] = [
            msg for msg in conversation["messages_list"] if msg["screen_name"] != "StoryBot"
        ]

    return conversations

# from kafka import KafkaConsumer
# import json
#
# KAFKA_TOPIC = "conversation_stream"
# KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # Update with actual Kafka server
#
# def load_conversation_data():
#     """Consumes messages from a Kafka stream and filters out messages from StoryBot."""
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
#
#         # Remove StoryBot messages
#         conversation["messages_list"] = [
#             msg for msg in conversation["messages_list"] if msg["screen_name"] != "StoryBot"
#         ]
#
#         conversations.append(conversation)
#         print(f"Received conversation: {conversation}")
#
#     return conversations

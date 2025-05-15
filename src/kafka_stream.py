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

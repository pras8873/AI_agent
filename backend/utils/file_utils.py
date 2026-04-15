import os

def create_topic_folder(topic):
    folder_name = topic.replace(" ", "_")
    path = os.path.join("output", folder_name)
    os.makedirs(path, exist_ok=True)
    return path

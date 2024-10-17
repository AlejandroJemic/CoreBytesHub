import  src.llm.llm_manager as llm
import json
import os
import src.utils as u

def get_text_from_entry(entry):
    (type,message) = u.check_path_or_url(entry)
    if message is not None:
        if message.startswith("Error"):
            print(message)
            return ""
        else:
            if type == "file":
                result = u.read_text_file(entry)
                if result is not None and result != "" and not result.startswith("Error"):
                    sumary = llm.sumarize_text(result) 
                    if sumary is not None:
                        return sumary
                    else:
                        print("Error al procesar el archivo")
                        return ""
                elif result.startswith("Error"):
                    print(result)
                    return ""
            elif type == "url":
                result = u.extract_text_from_url(entry)
                if result is not None and result != "" and not result.startswith("Error"):
                    sumary = llm.sumarize_text(result) 
                    if sumary is not None:
                        return sumary
                    else:
                        print("Error al procesar la URL")
                        return ""
                elif result.startswith("Error"):
                    print(result)
                    return ""
                    
            elif type == "text":
                return entry

def generate_note(jsonTopic, destination_folder, parentName=""):

    topicName = parentName + "-" + jsonTopic["name"].upper() if parentName != "" else jsonTopic["name"].upper()
    noteFileName = f"{topicName}.md"
    noteDirPath = os.path.join(destination_folder, topicName if not parentName else parentName)
    noteFilePath = os.path.join(noteDirPath, noteFileName)
    if os.path.exists(noteFilePath):
        print(f"Skipping {noteFileName} because it already exists")
        return
    print(f"anotating {jsonTopic['name']}")
    noteText = llm.generate_note_from_json(jsonTopic)
    if noteText is None:
        return
    else:
        if not os.path.exists(noteDirPath):
            os.makedirs(noteDirPath)
        print(f"Creating {noteFileName}")
        with open(noteFilePath, 'w') as f:
            f.write(noteText)

def main(entry):
    input_text = ""
    json_filename = "knowledge_map"
    destination_file = json_filename + ".json"
    destination_folder = "output"
    destination_path = os.path.join(destination_folder, destination_file)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    input_text = get_text_from_entry(entry)

    print("Generando JSON...")
    # Generar JSON
    json_output = llm.generate_json_from_text(input_text)
    if "topics" not in json_output:
        json_output = {"topics":json_output}

    print("JSON generado:")
    print(json.dumps(json_output, indent=2))
 
    u.update_or_create_json(destination_path, json_output)
    print(f"JSON guardado en {destination_file}")

    # iterante json topics and subtopics
    for topic in json_output["topics"]:
        data = {
            "name": topic["name"],
            "description": topic["description"],
        }
        generate_note(data, destination_folder)
        if topic["subTopics"] is  None:
            print("No subtopics found for: ", topic["name"])
        else:
            print("Subtopics found for: ", topic["name"])
            for subtopic in topic["subTopics"]:
                generate_note(subtopic, destination_folder, topic["name"].upper())

if __name__ == "__main__":
    while True:
        entry = input("Enter url, file path or text: ")
        main(entry)
        exit = input("Exit? (y/n): ")
        if exit.lower() == "y":
            break
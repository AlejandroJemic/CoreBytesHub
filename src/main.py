import  src.llm.llm_manager as llm
import json
import os
import src.utils as u

json_filename = "knowledge_map"
destination_file = json_filename + ".json"
destination_folder = "output"
destination_path = os.path.join(destination_folder, destination_file)
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

def get_text_from_entry(entry, relattedTo = ""):
    (type,message) = u.check_path_or_url(entry)
    if message is not None:
        if message.startswith("Error"):
            print(message)
            return ""
        else:
            if type == "file":
                result = u.read_text_file(entry)
                if result is not None and result != "" and not result.startswith("Error"):
                    sumary = llm.sumarize_text(result, relattedTo) 
                    if sumary is not None:
                        return sumary
                    else:
                        print("Error prossesing file")
                        return ""
                elif result.startswith("Error"):
                    print(result)
                    return ""
            elif type == "url":
                result = u.extract_text_from_url(entry)
                if result is not None and result != "" and not result.startswith("Error"):
                    sumary = llm.sumarize_text(result, relattedTo) 
                    if sumary is not None:
                        return sumary
                    else:
                        print("Error prossing URL")
                        return ""
                elif result.startswith("Error"):
                    print(result)
                    return ""
                    
            elif type == "text":
                return entry

def generate_note(index, jsonTopic, relattedTo, destination_folder, parentName=""):
    print(f"Generating note for {jsonTopic['name']}")
    if parentName != "":
        parentName = u.sanitize_filename(parentName)
    topicName = parentName + "-" + jsonTopic["name"].upper() if parentName != "" else jsonTopic["name"].upper()
    topicName = u.sanitize_filename(topicName)
    noteFileName = str(index).zfill(2) + "-" + f"{topicName}.md"
    noteDirPath = os.path.join(destination_folder, topicName if not parentName else parentName)
    noteFilePath = os.path.join(noteDirPath, noteFileName)
    if os.path.exists(noteFilePath):
        print(f"Skipping {noteFileName} because it already exists")
        return
    print(f"anotating {jsonTopic['name']}")
    noteText = llm.generate_note_from_json(jsonTopic, relattedTo)
    if noteText is None:
        return
    else:
        if not os.path.exists(noteDirPath):
            os.makedirs(noteDirPath)
        print(f"Creating {noteFileName}")
        with open(noteFilePath, 'w',encoding='utf-8') as f:
            f.write(noteText)

def generate_knowledge(entry, relattedTo):
    input_text = ""
    
    input_text = get_text_from_entry(entry, relattedTo)

    print("generating JSON...")
    # Generar JSONk
    json_output = llm.generate_json_from_text(input_text, relattedTo)
    if "topics" not in json_output:
        json_output = {"topics":json_output}

    print("JSON generated:")
    print(json.dumps(json_output, indent=2))
 
    u.update_or_create_json(destination_path, json_output)
    print(f"JSON saved at {destination_file}")

    process_pending_topics(relattedTo)

def process_pending_topics(relattedTo=""):
    # get topics from knowledge_map.json
    with open(destination_path, 'r') as f:
        knowledge_map = json.load(f)

    index = 0
    for topic in knowledge_map["topics"]:
        index += 1
        if topic["state"] != "pending":
            print("Skipping: ", topic["name"] + " state: " + topic["state"])
            continue
        try:
            data = {
                "name": topic["name"],
                "description": topic["description"],
            }
            generate_note(index, data, relattedTo, destination_folder)
            topic["state"] = "done"

            if topic["subTopics"] is  None:
                print("No subtopics found for: ", topic["name"])
            else:
                print("Subtopics found for: ", topic["name"])

                for subtopic in topic["subTopics"]:
                    index += 1
                    try:
                        generate_note(index, subtopic, relattedTo, destination_folder, topic["name"].upper())

                        subtopic["state"] = "done"
                       
                    except Exception as e:
                        print("Error processing subtopic: ", subtopic["name"] + ": " + str(e))

        except Exception as e:
            print("Error processing topic: ", topic["name"] + ": " + str(e))
            continue
    print("All topics DONE")
    u.replase_json(destination_path, knowledge_map)
    print("JSON updated")
    print("FINISH OK")

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- CORE BYTES HUB ---")
    print()

def handdle_generation():
    print_header()
    entry = input("Enter url, file path or text: ")
    relatedTo = input("Related to(some technology or anotation or empty): ")
    generate_knowledge(entry,relatedTo)

def main():
    print_header()
    while True:
        print("[K] Generate Knowledge")
        print("[P] Process pending topics")
        print("[E] Exit")
        selection = input("Select an option: ")
        if selection.lower() == "k":
            handdle_generation()
        elif selection.lower() == "p":
            process_pending_topics()
        elif selection.lower() == "e":
            print("EXIT 0")
            break
        else:
            print("Invalid option")
           
            continue

if __name__ == "__main__":
    main()
        

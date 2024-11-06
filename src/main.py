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

def get_subjects(entry):
    subjects = []
    if os.path.isfile(entry):          # check is is a validad filepath
        if os.path.exists(entry):
            with open(entry, 'r', encoding='utf-8') as f:
                  subjects = [line.strip() for line in f]
        else:
            return ('file',f"'Error: {entry}' is a valid filepath but does not exist.")
    else:
        subjects.append(entry)

    return subjects

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
    topicName = jsonTopic["name"].upper()
    topicName = u.sanitize_filename(topicName)  
    noteFileName = f"{index}-{topicName}.md"


    if parentName:
        noteDirPath = os.path.join(destination_folder, parentName) 
    else:
        noteDirPath = os.path.join(destination_folder, index + "-" + topicName)

    noteFilePath = os.path.join(noteDirPath, noteFileName)

    if os.path.exists(noteFilePath):
        print(f"Skipping {noteFileName} because it already exists")
        return

    print(f"Annotating {jsonTopic['name']}")
    noteText = llm.generate_note_from_json(jsonTopic, relattedTo)
    if noteText is None:
        return
    else:
        if not os.path.exists(noteDirPath):
            os.makedirs(noteDirPath)  
        print(f"Creating {noteFileName}")
        with open(noteFilePath, 'w', encoding='utf-8') as f:
            f.write(noteText)


def explain_subjetc(index, subject, destination_folder):
    
    print(f"Generating subject for {subject}")
   
    topicName = subject.replace("|", "-").upper()[0:50]
    topicName = u.sanitize_filename(topicName)
    noteFileName = index + "-" + f"{topicName}.md"
    noteDirPath = os.path.join(destination_folder)
    noteFilePath = os.path.join(noteDirPath, noteFileName)
    if os.path.exists(noteFilePath):
        print(f"Skipping {noteFileName} because it already exists")
        return
    print(f"anotating {subject}")
    noteText = llm.generate_note_from_text(subject)
    if noteText is None:
        return
    else:
        if not os.path.exists(noteDirPath):
            os.makedirs(noteDirPath)
        print(f"Creating {noteFileName}")
        with open(noteFilePath, 'w',encoding='utf-8') as f:
            f.write(noteText)

def process_pending_topics(relattedTo=""):
    # Cargar temas desde knowledge_map.json
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
            # Generar la nota del tema principal
            generate_note(str(index).zfill(2), data, relattedTo, destination_folder)
            topic["state"] = "done"

            if topic["subTopics"] is None:
                print("No subtopics found for: ", topic["name"])
            else:
                print("Subtopics found for: ", topic["name"])

                subIndex = 0
                for subtopic in topic["subTopics"]:
                    subIndex += 1
                    try:
                        # Generar notas para los subtemas, pero pasando el nombre del tema principal como `parentName`
                        generate_note(
                            f"{str(index).zfill(2)}-{str(subIndex).zfill(2)}",
                            subtopic,
                            relattedTo,
                            destination_folder,
                            topic["name"].upper()
                        )
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

def handle_subjects():
    print_header()
    entry = input("Enter url, file path or text: ")
    index = input("Start Index (or Enter for 0): ") 
    count = int(index)  if (index != "" and int(index) > 0) else 0
    for subject in get_subjects(entry):
        count += 1
        explain_subjetc(str(count).zfill(2), subject, destination_folder)

def main():
    print_header()
    while True:
        print("[K] Generate Knowledge")
        print("[P] Process pending topics")
        print("[S] Explain subject")
        print("[E] Exit")
        selection = input("Select an option: ")
        if selection.lower() == "k":
            handdle_generation()
        elif selection.lower() == "p":
            process_pending_topics()
        elif selection.lower() == "s":
            handle_subjects()
        elif selection.lower() == "e":
            print("EXIT 0")
            break
        else:
            print("Invalid option")
            continue

if __name__ == "__main__":
    main()
        

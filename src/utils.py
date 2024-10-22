import os
import re
import magic
import requests
import validators
import json
from bs4 import BeautifulSoup

import yaml



def read_config_file():
    print("Reading config file...")
    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    config_path = os.path.join(current_dir, 'config.yaml')

    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def check_path_or_url(input_string):
    print("Checking file path or URL...")
    # Verify if it's a filepath well formated
    if os.path.isfile(input_string):
        # check is is a validad filepath
        if os.path.exists(input_string):
            # return a tuple type, mesagge
            return ('file', f"'{input_string}' is a valid filepath and exists.")
        else:
            return ('file',f"'Error: {input_string}' is a valid filepath but does not exist.")
    # Verify if it's a valid URL
    elif validators.url(input_string):
        try:
            response = requests.head(input_string, timeout=5)
            if response.status_code == 200:
                return ('url',f"'{input_string}' is a valid URL and is accessible.")
            else:
                return ('url',f"'Error: {input_string}' is a valid URL but is not accessible. Status code: {response.status_code}.")
        except requests.RequestException as e:
            return ('url',f"'Error {input_string}' is a valid URL but could not be accessed. Error: {str(e)}")
    # If it's neither filepath nor URL
    else:
        return ('text',f"'{input_string}' is neither a valid filepath nor a valid URL.")



def replase_json(destination_path, json_output):
    print("Replasing JSON file...")
    if  os.path.exists(destination_path):
        os.remove(destination_path)
    with open(destination_path, 'w') as f:
        json.dump(json_output, f, indent=2)

def update_or_create_json(destination_path, json_output):
    print("Updating or creating JSON file...")
    
    if not os.path.exists(destination_path):
        with open(destination_path, 'w') as f:
            json.dump(json_output, f, indent=2)
    else:
        with open(destination_path, 'r+') as f:
            current_json = json.load(f)
            current_json["topics"].extend(json_output["topics"])
            f.seek(0)
            json.dump(current_json, f, indent=2)
            f.truncate()

def extract_text_from_url(input_string):
    print("Extracting text from URL...")
    try:
        response = requests.get(input_string, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            body_content = soup.body.get_text(separator=' ', strip=True)
            clean_text = ' '.join(body_content.split())
            return clean_text
        else:
            raise Exception(f"'{input_string}' is not accessible. Status code: {response.status_code}.")
    except Exception as e:
        return f"Error: {str(e)}"
    


def read_text_file(file_path):
    print("Reading text file " + file_path)
    mime_type = magic.from_file(file_path, mime=True)
    if mime_type and mime_type.startswith('text'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    else:
        return f"'Error {file_path}' is not a text file."


def sanitize_filename(filename):
    try:
        filename = filename.replace(' ', '_')
        filename = re.sub(r'[\/\(\)\[\]\{\}\*\\|?:]', '-', filename)
        return filename
    except Exception as e:
        print(f"Error sanitizing filename: '{filename}'. Error is:{str(e)}")
        return filename
    
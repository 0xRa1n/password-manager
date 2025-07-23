import time, os, json

from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# encryption is removed

def add_entry(website:str, username: str, password: str):
    with open("passwords.json", "r+", encoding="UTF-8") as file:
        payload = {
            "website": website,
            "credentials": {
                "username": username,
                "password": encrypt(password)
            }
        }

        file_data = json.load(file)
        file_data.append(payload)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
        return True

def delete_entry(username: str, password: str):
    with open("passwords.json", "r", encoding="utf-8") as f:
        file_json = json.load(f)

        check_existence = [
            users for users in file_json
            if users.get("credentials", {}).get("username") == username
        ]
        if len(check_existence) == 0:
            return "Entry is already gone"

        file_json = [
            users for users in file_json
            if users.get("credentials", {}).get("username") != username
        ]
        
        with open("passwords.json", "w", encoding="utf-8") as file:
            json.dump(file_json, file, indent = 4)
            return True
        
def view_entry():
    with open("passwords.json", "r", encoding="utf-8") as f:
        file_json = json.load(f)

        contents = [
            credentials for credentials in file_json
        ]
        return contents
    
def update_entry(original_website: str, original_username: str, new_username: str, new_password: str, new_website: str):
    with open("passwords.json", "r", encoding="utf-8") as f:
        file_json = json.load(f)

    for credentials in file_json:
        if credentials.get("credentials", {}).get("username") == original_username:
            credentials["website"] = new_website
            credentials["credentials"]["username"] = new_username
            credentials["credentials"]["password"] = encrypt(new_password)
            break 

    with open("passwords.json", "w", encoding="utf-8") as f:
        json.dump(file_json, f, indent=4)

        return True

import requests
import re
import base64 

token = ""
group_id = ""

def base64_detector(text):
    try:
        decoded_text = base64.b64decode(text).decode()
        print("Decoded text:", decoded_text)
    except Exception as e:
        print("Error decoding Base64:", e)

    print("Original text:", text)

def check_input(input):
    pattern = re.compile(r'(hegh|هق)\1*$', re.IGNORECASE | re.UNICODE)
    if pattern.match(input):
        print("Message contains 'هق'")
    else:
        print("Message does not contain 'هق'")

    base64_detector(input)

def get_updates(offset=None):
    telegram_api = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {'offset' : offset}
    response = requests.get(telegram_api, params=params)

    if response.status_code == 200:
        updates = response.json().get('result', [])
        print(updates)
        return updates
    else:
        print(f"Error: {response.status_code}")
        return []

def delete_message(chat_id, message_id):
    telegram_api = f"https://api.telegram.org/bot{token}/deleteMessage"
    params = {'chat_id': chat_id, 'message_id': message_id}
    response = requests.get(telegram_api, params=params)
    if response.status_code != 200:
        print(f"Error deleting message: {response.status_code}")

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update['update_id'] + 1
                message = update.get('message')
                if message and 'text' in message:
                    text = message['text']
                    check_input(text)
                    if re.search(r'(hegh|هق)', text, re.IGNORECASE):
                        delete_message(message['chat']['id'], message['message_id'])

if __name__ == "__main__":
    main()

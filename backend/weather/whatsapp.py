from jaseci.jsorc.live_actions import jaseci_action
from typing import Union
import requests
import json

@jaseci_action(act_group=["whatsapp_web"], allow_remote=False)
def parse_inbound_message(request: Union[list, dict]):
    # parses message request payload and returns extracted values
    # Payload Structure
    # payload = {
    #     "sender_number": '',
    #     "message_id": '',
    #     "author": '',
    #     "media_type": '',
    #     "sender_message": '',
    #     "audio_id": '',
    #     "location": {"latitude": 0, "longitude": 0, "address"},
    #     'document_id': '',
    #     "document_type": '',
    #     "sticker_id": '',
    #     "reaction": '',
    #     'image_id': '',
    #     'video_id': '',
    #     'contact': {'name': '', 'phone_number': ''},
    #     'interactive': {'interactive_id': '', 'interactive_title': ''}
    #     'poll_id': '',
    #     'selectedOption': '',
    # }
    payload = {}
    # #print(f"This is the request body: {request}")
    if request:
        try:
            data = request.get("body", {})

            if (not data["event"] in ["onmessage", "onpollresponse", "onack"]):
                return {}

            sender_number = data.get("from", "")
            message_id = data.get("id", {})
            event_type = data.get("dataType", data.get("event", ""))
            from_me = data.get("id", {})   # Added 'fromMe' in the return payload
            if (type(from_me) == dict):
                # from me
                from_me = from_me.get("fromMe", "")
            else:
                # set from_me false
                from_me = False

            media_type = data.get("type", "")  # add data type if we got it
            payload['media_type'] = data.get("type", "")
            payload['fromMe'] = from_me
            payload['event_type'] = event_type  # Update: Using 'dataType' as 'event_type'
            payload['sender_message'] = ""
            payload["author"] = ""
            payload["caption"] = ""
            payload["isGroup"] = False

            # images with captions
            caption = data.get('caption', '')

            if caption:
                # add caption if we got it
                payload['caption'] = caption

            if (media_type == "chat"):
                payload['sender_message'] = data.get("content", "")
                payload['media_type'] = media_type

                if (data["event"] == "onack"):
                    # add unpromted message
                    payload['sender_message'] = data.get("body", "")

            if (media_type == "ptt" or media_type == "audio"):
                payload['audio_id'] = data.get("body", "")
                payload['media_type'] = media_type

            if (media_type == "location"):
                payload['location'] = data.get("location", {})
                payload['media_type'] = media_type

            if (media_type == "document"):
                payload['sender_message'] = ""
                payload['media_id'] = data.get("content", "")
                payload['filename'] = data.get("filename", "")
                payload['media_type'] = media_type
                payload['mime_type'] = data.get("mimetype", "")

            if (media_type == "sticker"):
                payload["sticker_id"] = data.get("body", "")
                payload['document_id'] = data.get("body", "")
                payload['media_type'] = media_type

            if (event_type == "message_reaction"):
                payload['sender_message'] = data.get("body", "")
                payload['media_type'] = "reaction"

            if (media_type == "image"):
                payload["media_id"] = data.get("content", "")
                payload['media_type'] = media_type
                payload['filename'] = data.get("filename", "")
                payload['mime_type'] = data.get("mimetype", "")

            if (media_type == "video"):
                payload["media_id"] = data.get("content", "")
                payload['media_type'] = media_type
                payload['filename'] = data.get("filename", "")
                payload['mime_type'] = data.get("mimetype", "")

            if (event_type == "onpollresponse"):
                sender_number = data.get("sender", "")
                payload["poll_id"] = data.get("msgId", {}).get("_serialized", "")
                payload['selectedOptions'] = data.get("selectedOptions", "")
                payload['media_type'] = "vote_update"
                payload['fromMe'] = False

            if (media_type in ("contacts", "vcard")):
                payload["contact"] = data.get("body", "")
                payload['media_type'] = media_type

            if (payload):
                payload['sender_number'] = sender_number.replace("@c.us", "")
                payload["message_id"] = message_id
                payload["author"] = data.get("author", "").replace("@c.us", "")  # Extracting 'author'
                payload["agent_number"] = data.get("to", "").replace("@c.us", "")  # Extracting 'to'
                payload["sender_name"] = ""  # Placeholder for sender_name
                payload["sender_fname"] = ""  # Placeholder for sender_fname

                # set is group
                if (payload["author"] and payload["sender_number"]) and (payload["author"] != payload["sender_number"]) and (len(payload["author"]) != len(payload["sender_number"])):
                    # set isGroup to true
                    payload["isGroup"] = True

                # process sender name
                sender_name = data.get("notifyName", "")

                if (sender_name):
                    sender_tokens = sender_name.split()
                    payload["sender_name"] = sender_name
                    payload["sender_fname"] = sender_tokens[0]

        except Exception as e:
            print("unable to process message payload ", e)
    return payload


@jaseci_action(act_group=["whatsapp_web"], allow_remote=True)
def send_text_message(phone_number: str, message: str, api_url: str, api_key: str, sessionId: str, isGroup: bool = False, options: dict = {}, isNewsletter: bool = False):
    """
    send_text_message function sends a text-based message to the provided phone number using the WhatsApp API.

    Parameters:
        phone_number (str): The phone number to which the message will be sent.
        message (str): The text message content.
        api_url (str): The URL of the WhatsApp API.
        api_key (str): The API key for authentication.
        sessionId (str): The session ID for the request.
        options (dict, optional): Additional options for the message. Defaults to {}.
        isGroup (bool, optional): Whether the message is a group message. Defaults to False.
        isNewsletter (bool, optional): Whether the message is a newsletter message. Defaults to False.

    Returns:
        dict: The JSON response from the WhatsApp API after sending the message.
    """
    # send text based message to phone number
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # construct message payload
    data = json.dumps({
        "phone": phone_number,
        "isGroup": isGroup,
        "isNewsletter": isNewsletter,
        "message": message,
        "options": options
    })

    # send request to WhatsApp API
    response = requests.post(f"{api_url}/api/{sessionId}/send-message", data=data, headers=headers)

    # return response from WhatsApp API
    return response.json()

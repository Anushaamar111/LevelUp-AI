from twilio.rest import Client
import os


def send_whatsapp_message(message_text):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_whatsapp_from = os.getenv("FROM")  
    whatsapp_to = os.getenv("TO")           

    client = Client(account_sid, auth_token)

    max_length = 1500  # Leave some room for headers/emojis
    messages = [message_text[i:i + max_length] for i in range(0, len(message_text), max_length)]

    for i, part in enumerate(messages):
        header = f"🧠 LifeCoach Tasks Part {i+1}:\n\n" if len(messages) > 1 else ""
        client.messages.create(
            body=header + part,
            from_=twilio_whatsapp_from,
            to=whatsapp_to
        )

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from .models import user_push_token

cred = credentials.Certificate('/aquaworld_backend/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def send_push_notification(user_id, title, message):
    values = user_push_token.objects.filter(user=user_id).values('token')
    tokens =[d['token'] for d in values]
    if not tokens:
        return
    notification = messaging.Notification(title=title, body=message)
    messages = messaging.MulticastMessage(
        notification=notification,
        tokens=tokens,
    )
    
    response = messaging.send_multicast(messages)
    return response
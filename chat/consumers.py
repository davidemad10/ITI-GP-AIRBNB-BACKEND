import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ConversationMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,code):
        # Leave room

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            conversation_id = data['data']['conversation_id']
            sent_to_id = data['data']['sent_to_id']
            name = data['data']['name']
            body = data['data']['body']

            # Get the user from the WebSocket scope
            user = self.scope['user']

            if user.is_anonymous:
                await self.send(text_data=json.dumps({
                    'error': 'You must be logged in to send messages.'
                }))
                return

            # Remove the authentication check and proceed to save the message
            await self.save_message(conversation_id, body, sent_to_id, user)

            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'body': body,
                    'name': name
                }
            )

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, Text data: {text_data}")
        except Exception as e:
            print(f"Error in receive: {e}, Text data: {text_data}")

    # Broadcast message to WebSocket clients
    async def chat_message(self, event):
        body = event['body']
        name = event['name']

        await self.send(text_data=json.dumps({
            'body': body,
            'name': name
        }))
    
    

    # Save the message to the database
    @sync_to_async
    def save_message(self, conversation_id, body, sent_to_id, user):
        ConversationMessage.objects.create(
            conversation_id=conversation_id,
            body=body,
            sent_to_id=sent_to_id,
            created_by=user if user.is_authenticated else None  
        )

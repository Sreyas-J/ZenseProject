import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from .models import Document

class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.document_name = self.scope['url_route']['kwargs']['doc']
        self.group = self.scope['url_route']['kwargs']['group']

        self.room_group_name = f"{self.group}_{self.document_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_group_name)

        await self.accept()

        self.document,created = await sync_to_async(Document.objects.get_or_create)(
            group=self.group, name=self.document_name
        )
        if not created:
            initial_content = self.document.content
            await self.send(text_data=json.dumps({
                'content': initial_content
            }))

    async def receive(self, text_data):
        content = json.loads(text_data)['content']
        self.document.content = content
        print(content)
        await database_sync_to_async(self.document.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'document_content',
                'content': content
            }
        )

    async def document_content(self, event):
        content = event['content']
        await self.send(text_data=json.dumps({
            'content': content
        }))
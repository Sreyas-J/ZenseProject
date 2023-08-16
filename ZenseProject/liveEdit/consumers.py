import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from .models import Document
from videoCall.models import Group


class EditConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.document_name = self.scope['url_route']['kwargs']['doc']
        self.group_name = self.scope['url_route']['kwargs']['group']

        self.room_group_name = f"{self.group_name}_{self.document_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.document= await self.doc_query()


        await self.accept()

        if self.document.content:
            content_data = json.loads(self.document.content)
            first_insert = content_data['ops']
            print(first_insert)  # Now you can safely print the first insert
            await self.send(text_data=json.dumps({
                'content': first_insert
            }))

    @database_sync_to_async
    def doc_query(self):
        grp = Group.objects.get(name=self.group_name)
        document, created = Document.objects.get_or_create(name=self.document_name)

        # Check if the document is not already associated with the group
        if document not in grp.doc.all():
            grp.doc.add(document)  # Associate the document with the group

        return document

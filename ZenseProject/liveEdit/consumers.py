import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from .models import Document

# class DocumentConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.document_id = self.scope['url_route']['kwargs']['document_id']
#         self.room_group_name = f"document_{self.document_id}"

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()
#         print('hi')

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         content = json.loads(text_data)['content']
#         document = await self.get_document(self.document_id)
#         document.content = content
#         await document.save()

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'document_content',
#                 'content': content
#             }
#         )

#     async def document_content(self, event):
#         content = event['content']
#         await self.send(text_data=json.dumps({
#             'content': content
#         }))

#     @staticmethod
#     async def get_document(document_id):
#         return await Document.objects.get_or_create(id=document_id)

class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type':'connection established'
        }))

    async def receive(self,text_data):
        text_data_json=json.loads(text_data)
        message=text_data_json['content']
        print('content: ',message)

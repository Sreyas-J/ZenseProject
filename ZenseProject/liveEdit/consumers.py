import json
import re
import subprocess

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
            print(first_insert)
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
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        print("data ",data)
        try:
            delta=data['delta']
            # Check if the sender's channel name is the same as the current channel name            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'document_content',
                    'delta': delta,
                    'exclude_channel':self.channel_name
                }
            )

            await self.update_doc(data['content'])
        except KeyError:
            
            code=await self.get_code(data['code'])
            
            if code:
                output = await self.execute_code(code)
                await self.send(text_data=json.dumps({'output': output}))

    async def get_code(self, content):
        code = ""
        for i in range(len(content)):
            if i < len(content) - 1 and content[i + 1].get('attributes', {}).get('code-block'):
                code += f'{content[i]["insert"]}\n'
        print("code: ", code)
        return code


    async def execute_code(self, code):
        try:
            process = subprocess.Popen(
                ['python3', '-c', code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )
            stdout, stderr = process.communicate(timeout=10)

            if stdout:
                output = stdout
            else:
                output = stderr

        except subprocess.TimeoutExpired:
            output = "Execution timed out."
        except Exception as e:
            output = str(e)

        print("OUTPUT: ",output)

        return output

    @database_sync_to_async
    def update_doc(self, content):
        def escape_quotes(match):
            return match.group().replace('"', r'\"')
        
        content_json = json.dumps(content)
        updated_content_json = content_json.replace("'", "\"")

        escaped_content_json = re.sub(r'console\.log\("([^"]*)"\)', escape_quotes, updated_content_json)

        self.document.content = escaped_content_json
        print(self.document.content)
        self.document.save()

    async def document_content(self, event):
        delta = event['delta']
        exclude_channel = event.get('exclude_channel')

        if exclude_channel != self.channel_name:
            # Send the message only to channels that are not excluded
            await self.send(text_data=json.dumps({
                'delta': delta
            }))
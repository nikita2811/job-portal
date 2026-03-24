# jobs/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

class JobConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user       = self.scope['user']
        self.group_name = 'latest_jobs'

        # reject unauthenticated users
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        # join the jobs group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"{self.user.email} connected to jobs feed")

        # send existing latest jobs on connect
        jobs = await self.get_latest_jobs()
        await self.send(text_data=json.dumps({
            'type':  'initial_jobs',
            'jobs':  jobs
        }))

    async def disconnect(self, close_code):
        # leave the jobs group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"{self.user.email} disconnected")

    async def receive(self, text_data):
        # handle messages from client if needed
        data = json.loads(text_data)
        if data.get('type') == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))

    # handler for new_job event broadcast
    async def new_job_posted(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_job',
            'job':  event['job']
        }))

    @database_sync_to_async
    def get_latest_jobs(self):
        from .services import get_latest_jobs_qs
        return get_latest_jobs_qs(user=self.scope['user'])
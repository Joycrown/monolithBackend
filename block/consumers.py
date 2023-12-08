from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from block.api.serializers import PostCountSerializer, BlockCountSerializer, CommentCountSerializer
from block.models import Post, Block, Comment
from core.models import User
from core.api.serializers import UserCountSerializer


def get_posts_data(postId):
    posts = Post.objects.filter(id__in=postId)
    serializer = PostCountSerializer(posts, many=True)
    return serializer.data

def get_comments_data(commentId):
    comments = Comment.objects.filter(id__in=commentId)
    serializer = CommentCountSerializer(comments, many=True)
    return serializer.data

def get_block_data(blockId):
    blocks = Block.objects.filter(id__in=blockId)
    serializer = BlockCountSerializer(blocks, many=True)
    return serializer.data


def get_user_data(username):
    user = User.objects.filter(username=username)
    if user.exists():
        serializer = UserCountSerializer(user, many=True)
        return serializer.data
    return

class TimelineConsumer(WebsocketConsumer):

    def fetch_post(self, data):
        updates = get_posts_data(data['postsId'])
        if updates:
            content = {
                'command': 'fetch_post',
                'update': updates
            }
            self.send_message(content)

    def fetch_comment(self, data):
        updates = get_comments_data(data['commentsId'])
        if updates:
            content = {
                'command': 'fetch_comment',
                'update': updates
            }
            self.send_message(content)        
    
    def fetch_block(self, data):
        updates = get_block_data(data['blockId'])
        content = {
            'command': 'fetch_block',
            'update': updates
        }
        self.send_message(content)

    def fetch_user(self, data):
        updates = get_user_data(self.room_name)
        content = {
            'command': 'fetch_user',
            'update': updates
        }
        self.send_message(content)

    commands = {
        'fetch_post': fetch_post,
        'fetch_comment': fetch_comment,
        'fetch_block': fetch_block,
        'fetch_user': fetch_user,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'timeline_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)      
        ## data from client
        # postsId
        # command
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

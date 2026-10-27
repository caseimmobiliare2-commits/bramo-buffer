import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from zoneinfo import ZoneInfo

TOKEN = os.getenv('BUFFER_API_KEY', '').strip()
CHANNEL = os.getenv('BUFFER_CHANNEL_ID', '').strip()
if not TOKEN or not CHANNEL:
    sys.exit('Missing BUFFER_API_KEY or BUFFER_CHANNEL_ID')

today = datetime.now(ZoneInfo('Europe/Zurich')).date().isoformat()
posts = json.loads(Path(__file__).with_name('posts.json').read_text(encoding='utf-8'))
selected = [p for p in posts if p['date'] == today]
if not selected:
    print(f'No approved posts for {today}; nothing to publish.')
    sys.exit(0)
if len(selected) > 1:
    sys.exit(f'Multiple posts on {today}: stop to avoid accidental posting')

post = selected[0]
query = '''mutation SendPost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id text dueAt } }
    ... on MutationError { message }
  }
}'''
variables = {'input': {
    'text': post['text'],
    'channelId': CHANNEL,
    'schedulingType': 'automatic',
    'mode': 'addToQueue'
}}
body = json.dumps({'query': query, 'variables': variables}).encode('utf-8')
request = Request('https://api.buffer.com', data=body, headers={
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
}, method='POST')
try:
    with urlopen(request, timeout=30) as r:
        response = json.load(r)
except HTTPError as exc:
    sys.exit(f'Buffer HTTP {exc.code}: {exc.read().decode()[:600]}')
if response.get('errors'):
    sys.exit(f'Buffer GraphQL error: {response["errors"]}')
result = response.get('data', {}).get('createPost', {})
if not result.get('post', {}).get('id'):
    sys.exit(f'Buffer did not create post: {result}')
print(f"Queued Buffer post ID {result['post']['id']} for local date {today}")

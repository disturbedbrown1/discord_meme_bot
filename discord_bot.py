import discord
from discord.ext import commands
import os
import requests
import praw
import logging
import random
import shutil


if not 'memes' in os.listdir():
    os.mkdir('memes')
os.chdir('memes')

logging.basicConfig(filename='logs.txt', level=logging.ERROR,
                    format='%(asctime)s -  %(levelname)s -  %(message)s')

client_id = 'your-client-id'
client_secret = 'your-secret'
user_agent = 'windows:com.example.prawmemes:v0.1 (by /u/your-username)'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)


def save_memes():
    """ saves memes locally from reddit r/memes """

    for submission in reddit.subreddit('memes').new(limit=10):
        try:
            meme_url = submission.url
            meme_title = submission.title

            # Use stream = True to guarantee no interruptions.
            r = requests.get(meme_url, stream=True)
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            with open(f'{meme_title}.jpg', 'wb') as handler:
                shutil.copyfileobj(r.raw, handler)
        except:
            logging.error('\nAn error occured with file ' +
                          (submission.title) + ' (' + (submission.url) + ')')


def get_memes():
    """ gets a list of all memes saved locally and chooses a random meme to send """

    meme_list = os.listdir()

    for f in meme_list:
        if not f.endswith('.jpg'):
            meme_list.remove(f)

    meme_to_send = random.choice(meme_list)

    return meme_to_send


TOKEN = 'your-token'

client = discord.Client()


@client.event
async def on_ready():
    print('bot is up and running!!')


@client.event
async def on_message(message):
    if message.content == '.meme':
        await message.channel.send(f'sending a meme your way! {message.author.mention}')
        meme = get_memes()

        with open(meme, 'rb') as meme_jpg:
            await message.channel.send(file=discord.File(meme_jpg))

    if message.content == '.omg':
        await message.channel.send('kalat baat')
        await message.delete(delay=2)

    if message.content == '.save':
        save_memes()
        await message.channel.send('getting some memes!')

client.run(TOKEN)

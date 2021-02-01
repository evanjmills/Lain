import asyncio
import os
import json
import random
from urllib.request import urlopen
from urllib.error import HTTPError

from bs4 import BeautifulSoup as bs
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix='>')


async def scrape_anime(user):
    url = f'https://myanimelist.net/animelist/{user}?status=6'

    try:
        bs_client = urlopen(url)
        page = bs_client.read()
        bs_client.close()

        soup = bs(page, 'html.parser')

        anime_list = soup.findAll('table', {'class', 'list-table'})
        anime_list = json.loads(anime_list[0]['data-items'])
        partial_url = anime_list[random.randint(0, len(anime_list) - 1)]['anime_url']
        anime_url = f'https://myanimelist.net/{partial_url}'
        return f'I recommend {anime_url}'
    except Exception:
        return f'I could not find {user}\'s plan to watch list. Make sure the list is set to public.'


@client.event
async def on_ready():
    print('Connected')


@client.command()
async def rec(ctx):
    mal_user = ctx.message.content
    mal_user = mal_user.replace('>rec ', '')
    await ctx.message.channel.send(f'Let me check out {mal_user}\'s plan to watch list')
    await ctx.message.channel.send(await scrape_anime(mal_user))

client.run(TOKEN)

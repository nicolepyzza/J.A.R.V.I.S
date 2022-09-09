import discord
import os
import random
import time

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
USER1_TOKEN = os.getenv('NICOLE_ID')
USER2_TOKEN = os.getenv('COLIN_ID')

## IMPORT MESSAGES
from messages import random_phrases
from messages import woops

## BOT intents
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def random_message():
  return random.choice(random_phrases)

async def random_apology():
  return random.choice(woops)

async def check_status(admin1, admin2):
  print('Checking if Admins are online...')
  if admin1.status == discord.Status.online and admin2.status != discord.Status.online:
    print('Admin1 is online')
    return 'user1'
  elif admin2.status == discord.Status.online and admin1.status != discord.Status.online:
    print ('Admin2 is online')
    return 'user2'
  elif admin2.status == discord.Status.online and admin1.status == discord.Status.online:
    print('Both are online!')
    return 'both'
  else:
    return 'none'

async def send_messages(member, guildid):
  guild = client.get_guild(guildid)

  user1 = guild.get_member(int(USER1_TOKEN))
  user2 = guild.get_member(int(USER2_TOKEN))
  res = await check_status(user1, user2)
  message = f'{member} is in the waiting room.'

  if res == 'both':
    await user1.send(message)
    await user2.send(message)
  elif res == 'user1':
    await user1.send(message)
  elif res == 'user2':
    await user2.send(message)
  else:
    return 'offline'


@client.event
async def on_voice_state_update(member, before, after):
  try:
    channel = discord.utils.get(member.guild.voice_channels, name='General')
    if after.channel.id == channel.id:
        msg = await random_message()
        await member.guild.system_channel.send(msg)
        offline = await send_messages(member.name, member.guild.id)
        if offline == 'offline':
          sry = await random_apology()
          time.sleep(3)
          await member.guild.system_channel.send(sry)
        print('done')
    if member.guild.name != 'test server':
      print('Member moved servers.')
  except:
    print('ERROR')

client.run(TOKEN)
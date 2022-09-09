from turtle import reset
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
from jarvis import hello, acceptable_greetings, here

## BOT intents
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def random_message(array):
  return random.choice(array)

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

  # if member not in str(user1) or member in str(user2):
  if res == 'both':
    await user1.send(message)
    await user2.send(message)
  elif res == 'user1':
    await user1.send(message)
  elif res == 'user2':
    await user2.send(message)
  else:
    return 'offline'
  # else:
  #   print('User is Admin, no message sent.')

@client.event
async def on_voice_state_update(member, before, after):
  try:

    channel = discord.utils.get(member.guild.voice_channels, name='General')

    if after.channel.id == channel.id:
      msg = await random_message(random_phrases)
      await member.guild.system_channel.send(msg)
      res = await send_messages(member.name, member.guild.id)

      if res == 'offline':
        #generate message
        sry = await random_message(woops)
        #sleep for 3 sec
        time.sleep(3)
        #send message
        await member.guild.system_channel.send(sry)

      print('done')
    
  except:
    print('error')
    # Exception as e:
    #   print(e)


@client.event
async def on_message(message):

  #if @J.A.R.V.I.S is mentioned in message
  if '<@1016853519543844944>' in message.content:
    
    #note the channel
    msg_channel = message.channel
    msg = message.content.lower()
    
    if any(greeting in msg for greeting in acceptable_greetings): 
      # generate a random greeting
      res = await random_message(hello)

      # check if MEMBER needs to be replaced with username
      new_res = await replace_member(res, message.author)
      
      await msg_channel.send(new_res)


async def replace_member(res, author):
  search_text = 'MEMBER'
  replace_text = str(author).split('#', 1)

  if search_text in res:
    new_res = res.replace(search_text, replace_text[0])
  else:
    new_res = res

  return new_res

client.run(TOKEN)
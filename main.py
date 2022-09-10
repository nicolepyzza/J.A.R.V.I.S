import discord
import os
import random
import time

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
USER1_TOKEN = os.getenv('NICOLE_ID')
USER2_TOKEN = os.getenv('COLIN_ID')
CHANNEL = os.getenv('CHANNEL_NAME')
TEXT_CHANNEL_ID = os.getenv('TEXT_CHANNEL_ID')
TEXT_CHANNEL = os.getenv('TEXT_CHANNEL')

## IMPORT MESSAGES
from messages import random_phrases, woops
from jarvis import hello, acceptable_greetings, here

## intents
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

async def random_message(array):
  try:
    print('Generating random message...')
    return random.choice(array)
  except:
    print('Error generating random message.')

async def check_status(admin1, admin2):
  try:
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
  except:
    print('Error checking if admins are online.')

async def check_if_admin(member, admin1, admin2):
  try:
    print('Checking if member is an admin...')
    print(f'Admin1: {admin1}, Admin2: {admin2}, Member: {member}')
    if member in str(admin1) or member in str(admin2):
      return True
    else:
      return False
  except:
    print('Error checking if member is one of the admins.')

async def send_messages(member, admin1, admin2):
  try:
    print('In send_messages func...')
    # check the onlien status of both admins
    res = await check_status(admin1, admin2)

    # define message being sent to admins
    message = f'{member} is in the waiting room.'

    if res == 'both':
      await admin1.send(message)
      await admin2.send(message)
    elif res == 'user1':
      await admin1.send(message)
    elif res == 'user2':
      await admin2.send(message)
    else:
      return 'offline'

  except:
    print('Error in send_messages func.')

async def replace_member(res, author):
  try:
    print('Replacing member variable...')
    # define what variable to search for within message
    search_text = 'MEMBER'

    #grab authors full name (e.g. user#1234), split before # and only pull 0 in array
    replace_text = str(author).split('#', 1)

    # if the variable is within the string, replace with username
    if search_text in res:
      new_res = res.replace(search_text, replace_text[0])
    else:
      new_res = res

    return new_res
  except:
    print('Error replacing variable.')

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
  try:
    print('Voice state update invoked...')

    ## define guild, admins, channels
    guild = client.get_guild(member.guild.id)
    admin1 = guild.get_member(int(USER1_TOKEN))
    admin2 = guild.get_member(int(USER2_TOKEN))
    channel = discord.utils.get(member.guild.voice_channels, name=CHANNEL)
    text_channel = discord.utils.get(member.guild.text_channels, name=TEXT_CHANNEL)

    # Check if Member is Admin
    is_admin = await check_if_admin(member.name, admin1, admin2)

    # if member is NOT an admin
    if is_admin == False:
      print('Member is NOT admin')
      # If channel joined == channel specified in env
      if channel.name == CHANNEL:

        # generate random message
        msg = await random_message(random_phrases)

        # replace variables if necessary
        new_msg = await replace_member(msg, member)
        
        # J.A.R.V.I.S sends message to channel to alert member
        print('Sending message to alert member...')
        send_msg_mem = await text_channel.send(new_msg)

        # J.A.R.V.I.S sends DMs to admins
        res = await send_messages(member.name, admin1, admin2)

        if res == 'offline':

          # Generate apology message to member
          sry = await random_message(woops)

          # Sleep for 5 sec
          time.sleep(5)

          # Send apology message to channel
          await member.guild.system_channel.send(sry)

        print('done')
    else:
      print('Member is Admin.')

  except:
    print('Error on_voice_state_update.')

@client.event
async def on_message(message):
  try:
    print('On messages invoked...')
    #if @J.A.R.V.I.S is mentioned in message
    if '<@1016853519543844944>' in message.content:
      
      print('J.A.R.V.I.S was tagged...')
      # define message channel
      msg_channel = message.channel

      # lowercase all message content
      msg = message.content.lower()
      
      # if greeting is within the message content
      if any(greeting in msg for greeting in acceptable_greetings): 
        # generate a random greeting
        res = await random_message(hello)
        print(f'got message: {res}')

        # check if MEMBER needs to be replaced with username
        new_res = await replace_member(res, message.author)
        print(f'got new msg: {new_res}')
        
        await msg_channel.send(new_res)
    else:
      print('J.A.R.V.I.S was not tagged in message content.')
  except:
    print('Error on_message.')

client.run(TOKEN)
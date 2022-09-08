import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
USER1_TOKEN = os.getenv('NICOLE_ID')
USER2_TOKEN = os.getenv('COLIN_ID')

## BOT intents
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')    

async def check_status(user1, user2):
  print('Checking if Admins are online...')
  if user1.status == discord.Status.online and user2.status != discord.Status.online:
    print('Admin1 is online')
    return 'user1'
  elif user2.status == discord.Status.online and user1.status != discord.Status.online:
    print ('Admin2 is online')
    return 'user2'
  elif user2.status == discord.Status.online and user1.status == discord.Status.online:
    print('Both are online!')
    return 'both'
  else:
    return 'No one is online'

async def send_messages(member, guild):
  guild = client.get_guild(guild)
  user1 = guild.get_member(USER1_TOKEN)
  user2 = guild.get_member(USER2_TOKEN)
  res = await check_status(user1, user2)

  if res == 'both':
    await user1.send(f'{member} is in the waiting room.')
    await user2.send(f'{member} is in the waiting room.')
  elif res == 'user1':
    await user1.send(f'{member} is in the waiting room.')
  elif res == 'user2':
    await user2.send(f'{member} is in the waiting room.')
  else:
    return 'offline'


@client.event
async def on_voice_state_update(member, before, after):
  try:
    channel = discord.utils.get(member.guild.voice_channels, name='General')
    if after.channel.id == channel.id:
        await member.guild.system_channel.send(f'Hi, {member.name}! I\'ve alerted someone that you\'re in the waiting room. Hang tight, buddy.')
        offline = await send_messages(member.name, member.guild.id)
        if offline == 'offline':
          await member.guild.system_channel.send('Sorry, no one\'s home to let you in :(')
        print('done')
  except:
    print('Member moved servers.')

client.run(TOKEN)
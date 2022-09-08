import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')    

members = discord.utils.get(client.get_all_members(), guild__name='test server', name='General')

async def check_status(nicole, colin):
  print('Checking if Colin & Nicole are online...')
  if nicole.status == discord.Status.online and colin.status != discord.Status.online:
    print('Nicole is online')
    return 'nicole'
  elif colin.status == discord.Status.online and nicole.status != discord.Status.online:
    print ('Colin is online')
    return 'colin'
  elif colin.status == discord.Status.online and nicole.status == discord.Status.online:
    print('Both are online!')
    return 'both'
  else:
    return 'No one is online'

async def send_messages(member, guild):
  guild = client.get_guild(guild)
  colin = guild.get_member(235537675778523136)
  nicole = guild.get_member(346823964909371393)

  res = await check_status(nicole, colin)

  if res == 'both':
    await nicole.send(f'{member} is in the waiting room.')
    await colin.send(f'{member} is in the waiting room.')
  elif res == 'nicole':
    await nicole.send(f'{member} is in the waiting room.')
  elif res == 'colin':
    await colin.send(f'{member} is in the waiting room.')
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
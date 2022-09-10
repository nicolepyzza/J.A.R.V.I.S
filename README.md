# J.A.R.V.I.S
A customizable bot built with Python and deployed with Heroku

### About

### Features
* Doorbell: When a user joins the voice channel specified, J.A.R.V.I.S will send a message in the general text channel and alert the users of your choice, as specified in the .env file.

### Usage
Prior to use, customize this bot and make it your own. Ensure you follow the [proper Discord Bot steps here](https://discordpy.readthedocs.io/en/stable/discord.html).

Running J.A.R.V.I.S locally:
1. Fork this repository
2. Create a .env file with the appropriate variables
3. Run the following command:
```
sh .\run.sh
```

Running J.A.R.V.I.S on Heroku:
1. Fork this repository
2. In your Heroku settings for your application, set the environmental variables as specified below:
```
TOKEN = Token for your bot, which will be set when you follow the Discord Bot steps above.
USER1_TOKEN = ID of admin (or person that will be notified)
USER2_TOKEN = OPTIONAL, if more than 1 admin needs to be specified.
CHANNEL = Channel name of the voice channel you want to watch
TEXT_CHANNEL_ID = Text channel for where you want to send messages
TEXT_CHANNEL = Name of the text channel for where you want to send messages
JARVIS_ID = ID of your bot, formatted as '<@48948309849324>'
```
3. Ensure worker dynos are enabled
4. Deploy

### How to get IDs in Discord
1. Go to your Discord settings and ensure Developer Mode is set to True.
2. Right click any channel, server, or member and select "Copy ID"

### License
Released under the [Apache License 2.0](https://github.com/Spiderjockey02/Discord-Bot/blob/master/LICENSE) license.

### Upcoming Release (v2.0):
* Message when user joins the guild/server
* More interactions with J.A.R.V.I.S including jokes and general conversation

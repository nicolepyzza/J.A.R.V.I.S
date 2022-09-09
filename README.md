# J.A.R.V.I.S
A customizable bot built with Python

### About

### Features
1. Doorbell
When a user joins the voice channel specified, J.A.R.V.I.S will send a message in the general text channel and alert the users of your choice, as specified in the .env file.

Example: 
UserA joins a public voice channel, General, while UserB and UserC are in a private voice channel that UserA cannot see. By joining General, J.A.R.V.I.S will alert admins that UserA should be moved to the private chat channel to join friends.

### Usage
Running J.A.R.V.I.S locally:
1. Fork this repository
2. Create a .env file with the appropriate variables
3. Run the following command:
```
sh run.sh
```

### License
Released under the [Apache License 2.0](https://github.com/Spiderjockey02/Discord-Bot/blob/master/LICENSE) license.


### TODO:
* msg when user switches servers after joining waiting room
* random messages
* check if admins are online AND in the guild
----
* jarvis calls
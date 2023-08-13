# SyncBot

Version -- SyncBot v2.0 
*NEW* 
- Uses Postgresql-15 database to store pertinent information by Server.
- Allows server admin to make a personalized !create command.
- Allows server admin to make a !channel where a particular !create command can be used. 
- Allows server admin to !initialize a previously created channel to work with a !create command. 

When a user uses "!create groupType groupName" command, there's three things that happen:

1. A server role is created based on the groupName 
2. A server message is created in the appropriate channel, which will be modifiable by the admin (i.e. if !create groupType if used, depending on where admin set groupType to exist in the server, the standard message and reaction role will be posted there)
3. A text-channel is formed with the groupName as its title, and then its permissions are set to private so that only people with the groupName role can see it. 

Wehn an admin uses "!channel channelName groupType" command, 

1. A discord channel is created with the channelName
2. Users can now use !create groupType and posts will populate in that channelName 
3. Postgres database is updated to store that channel's information and what groupType is associated with it.

<hr> 

Version -- SyncBot v1.0 

Use the command !create groupName and let the bot handle the rest. This will:
- Create a new role named after your group. Used to distinguish members and create sub-groups within the server. 
- Set up a dedicated channel for the group. (Currently in a dedicated Category called "ROLE SPECIFIC CHANNELS 🔐")
- Generate a standardized post for others to join by reacting with a 👍. (Currently in a dedicate channel called #active-learning-groups)
- Keep track of number of members in learning group on post. 

## Example Usage:

!create stanfordcs229
It would be beneficial to get a general idea of the fundamentals used in ML before getting into creating models or using algorithms even. I'll be starting this course on Monday, August 14th. I'll pace myself at roughly 1 lecture per week. Each week I’d like to review and discuss with others who join.  

**Recommended Prerequisites:** Linear Algebra, Statistics/Probability (can be studied alongside if needed)
**Estimated Timeframe:** 5-8 Months 

📚 Intro to ML CS229 Stanford Course Options (Find detailed info in ⁠stanfordcs229 pins after you react):
https://tinyurl.com/2018CS229 (2018 CS229 Playlist) by Andrew Ng
https://tinyurl.com/2019CS229 (2019 CS229 Playlist) by Anand Avati 
https://tinyurl.com/2022CS229 (2022 CS229 Playlist) by Tengyu Ma

## Example Result:

<img width="1137" alt="image" src="https://github.com/rohitmit98/SyncBot/assets/51212933/a2920578-4e0a-4354-a53f-d82d1cb9209e">

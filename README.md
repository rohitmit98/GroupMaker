<hr>
Version -- GroupMaker (SyncBot v2.0)

*NEW FEATURES* 
- Rename to be have a more accurate description
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
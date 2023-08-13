Dev notes:

- postgres running successfully on linux vm
- psql to initiate postgres comamnds
- need to create tables in postgres that will store server_id, role_id, message_id, channel_is(s), and groupType, and groupName. Here is the structure:

# servers Table:
server_id: The unique ID of the Discord server.

# command_channels Table:
server_id: The ID of the Discord server this channel belongs to.
channel_id: The unique ID of the channel where certain bot commands can be used.
channel_name: Name of the channel. This is mainly for human readability and ease of management.
group_type: The type of group (e.g., "study", "project") that can be created in this channel. This helps in defining context for bot commands.
message_id: The unique ID of the message. This is crucial for tracking and possibly manipulating (e.g., deleting, editing) bot-created messages in the future.

NOTE: if a single channel supports multiple group types, that would indeed mean multiple rows with the same channel_id and channel_name but different group_type entries.

# roles Table:
server_id: The ID of the Discord server this role belongs to.
role_id: The unique ID of the Discord role.

# messages Table:
server_id: The ID of the Discord server where this message was posted.
channel_id: The channel where this message was posted.

# text_channels Table:
server_id: The ID of the Discord server this channel belongs to.
channel_id: The unique ID of the text channel.
role_id: The role ID that has access to this channel. This provides a quick reference for permissions and role-specific actions.


Other considerations:
1. Server Joins/Leaves: When your bot joins a server, you can have an initialization routine that sets up basic defaults in the database for that server. Conversely, when the bot is removed from a server, you might consider cleaning up or archiving related entries.

2. Consistent Data Entry: Ensure consistency in data entry, especially when it comes to linking tables through common keys like server_id, channel_id, etc.

3. Normalization: You've done a good job keeping the data structures normalized. This reduces data redundancy and improves data integrity. Just keep an eye out as you expand your bot's features to avoid unintentionally denormalizing your database.

4. Backups & Maintenance: Always have a backup and maintenance plan for your database. It's not just about structuring data, but also about ensuring its safety and long-term sustainability.

Once I have these tables set up in your database, the next step will be to integrate your bot code to interact with this database. This will involve setting up a database connection, writing queries to fetch and store data, and handling any potential database errors.

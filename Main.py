

import discord
from discord import Intents, Message





token:str = 'token'
admin_user_name:str = 'admin'


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

async def getMessages(channel, limit:int, filter:str = None):
    """
    Fetches messages from a given channel, filtered by a given keyword.

    Args:
        channel (discord.TextChannel): The channel to fetch messages from.
        limit (int): The maximum number of messages to fetch.
        filter (str, optional): If given, only messages containing this keyword will be returned.

    Returns:
        List[discord.Message]: A list of messages, filtered by the given keyword if applicable.
    """
    messages = []
    async for msg in channel.history(limit=limit):
        if msg.author != client.user:
            if '-' in msg.content or '~' in msg.content and msg.author!= client.user:
                messages.append(msg)
    if filter==None:
        return messages

    else:
        res= [msg for msg in messages if filter in msg.content]
        if len(res) ==0:
            await channel.send('No results found :/')

        return res


async def handle_commands(message:Message):

    """
    Handles commands sent to the bot.

    This function is called every time a message is sent to a channel the bot is in.
    It checks if the message is a command, and if so, it executes the corresponding code.

    Currently, the bot supports the following commands:
    - `QBot fetchQuotes`: Fetches all quotes from the channel and sends them back.
    - `QBot fetchQuotes with <search_term>`: Fetches all quotes from the channel that contain the given search term and sends them back.
    - `QBot bully <user_name>`: Sends a message saying that the user is short.
    """
    if message.content.startswith("QBot"):
        command_tokens = message.content.split(" ")
        if command_tokens[1] == "fetchQuotes" and message.channel.name == 'quotes':
           if len(command_tokens) <= 3 and not message.reactions:
                message_list = await getMessages(message.channel, 1000)
                for m in message_list:
                    await message.channel.send(m.content)
                await message.add_reaction('👍')

           else:
                if command_tokens[2] == 'with' and not message.reactions:
                    search_term = command_tokens[3]
                    message_list = await getMessages(message.channel, 1000, search_term)
                    for m in message_list:
                        await message.channel.send(m.content)
                    await message.add_reaction('👍')
        elif command_tokens[1] == 'bully' and len(command_tokens) == 3:
            members = message.channel.members
            if command_tokens[2] == admin_user_name:
                await message.channel.send(f'You dare use my own spells against me, {message.author.mention}?! ')
                await message.add_reaction('👎')

            elif command_tokens[2] == 'QBot':
                await message.channel.send(f'Why are you being mean to QBot 😭😭😭😭 ? \n {message.author.mention} is a MONSTER !!')
            else:
                try:
                    member = next(m for m in members if m.name == command_tokens[2])
                    await message.channel.send(f'{member.mention} is short :)')
                    await message.add_reaction('👍')
                except StopIteration:
                    await message.channel.send(f'User \"{command_tokens[2]}\" not found :/')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



@client.event
async def on_message(message):


    if message.author == client.user:
        return
    await handle_commands(message)





client.run(token)

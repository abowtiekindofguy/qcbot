# This example requires the 'message_content' intent.

import discord,csv
import matplotlib.pyplot as plt
intents = discord.Intents.default()
intents.message_content = True
from teams import Team,AllTeams
client = discord.Client(intents=intents)
Teams=AllTeams()
recordfile='record.csv'
def writetocsv(filename,content):
    with open(filename,'a') as csvfile:
        qcwriter=csv.writer(csvfile)
        qcwriter.writerow(content)
def get_substring_between_hashes(string):
    first_hash_index = string.find("#")
    second_hash_index = string.find("#", first_hash_index + 1)

    if first_hash_index != -1 and second_hash_index != -1:
        substring = string[first_hash_index + 1 : second_hash_index]
        return substring

    return None
def bold_display(x):
    start = "**"
    end = "**"
    return start+str(x)+end
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('Initializing Teams')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        message_author=message.author
        timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        message_content=message.content
        writetocsv(recordfile,['gen',timestamp,message_author,message_content])
    if message.content.startswith('!pounce'):
        message_author=message.author
        timestamp=message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        message_content=message.content
        writetocsv(recordfile,['pounce',timestamp,message_author,message_content])
    if message.content.startswith('!createteam '):
        message_author=message.author
        team_name=get_substring_between_hashes(message.content.strip('!createteam '))
        newteam=Team(team_name)
        tagged_users=message.mentions
        for user in tagged_users:
            newteam.add_member(user.id)
        Teams.add_team(team_name,newteam)
        reply_content = f"Hey there {message_author.mention}, your team "+bold_display(team_name)+" with "+f"{', '.join([user.mention for user in tagged_users])}"+" is registered! We wish you accepted pounces ;)"  
        print(Teams)
        await message.channel.send(reply_content)
    if message.content.startswith('!createteamrole'):
        message_author=message.author
        message_content=message.content
        team_name=get_substring_between_hashes(message_content)
        role = await message.guild.create_role(name=team_name)
        if role is not None:
            await message_author.add_roles(role)
            await message.channel.send(f"Role {role.name} assigned to {message_author.mention}")
        else:
            await message.channel.send(f"Role {team_name} does not exist!")

    if message.content.startswith('!joinvc'):
        message_author=message.author
        team_name=message.author.role
        voice_channel=client.get_channel(team_name)
        if voice_channel is not None and isinstance(voice_channel, discord.VoiceChannel):
            if message_author.voice is not None and message_author.voice.channel is not None:
                await message_author.voice.channel.disconnect()
            await message_author.move_to(voice_channel)
            await message.channel.send(f"{message_author.mention} has been connected to VC: {voice_channel.name}")
        else:
            await message.channel.send("Invalid or non-existent voice channel.")

    if message.content.startswith('!create_voice_channels'):
        names = ['UselessLogs', 'Name2', 'Name3']  # Specify the names for the voice channels

        # Create voice channels for each name in the list
        for name in names:
            # Create the voice channel
            new_channel = await message.guild.create_voice_channel(name)

            # Set permissions to allow only users with roles matching the channel names
            for role in message.guild.roles:
                if role.name == name:
                    await new_channel.set_permissions(role, connect=True, speak=True)
                else:
                    await new_channel.set_permissions(role, connect=False, speak=False)

        await message.channel.send(f"Voice channels created for each name.")

    if message.content.startswith('!delete_voice_channels'):
        channel_names = ['UselessLogs', 'Name2', 'Name3']  # Specify the names of the voice channels to delete

        # Delete voice channels with matching names
        for voice_channel in message.guild.voice_channels:
            if voice_channel.name in channel_names:
                await voice_channel.delete()

        await message.channel.send("Voice channels deleted.")
    
    if message.content.startswith('!deleteallroles'):
        for role in message.guild.roles:
            if role.name != "@everyone":
                await role.delete()
        await message.channel.send('All roles have been deleted!')


    if message.content.startswith('!showplot'):
        message_content=message.content
        toplot=message_content.strip('!showplot')
        toplot1,toplot2=toplot.split(':')
        X=toplot1.split()
        Y=toplot2.split()
        plt.plot(X, Y)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('My Graph')
        plt.savefig('graph.png')
        
        # Load the saved image
        file = discord.File("graph.png", filename="graph.png")

        # Send the image as a message
        await message.channel.send(file=file)

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

client.run(token)

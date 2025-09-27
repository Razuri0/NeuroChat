from utils.GPT_Bot_Framework import GPT_completion
import discord
from discord.ext import commands, tasks
from utils.youtube_downloader import yt_downloader
import re
import random
import asyncio
import matplotlib.pyplot as plt
import time
from collections import defaultdict
from datetime import datetime
from gtts import gTTS
import os
from datetime import datetime, timedelta

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Prefix = "%"
intents = discord.Intents.all()
client = commands.Bot(command_prefix=Prefix, intents=intents)

# Discord API key
with open("discord_key", "r") as file:
    key = file.read().strip()

# OpenAI API key
with open("openai_key", "r") as file:
    API = file.read().strip()

# AI settings
AI = "gpt-5-nano"
# AI = "gpt-5"
Bot_Name = "NeuroChat"
# GPT settings
n, temperature, model, max_Tokens = 1, 0.8, AI, 200000

pre_prompt_main = [{"role": "user", "content": f"You're name is {Bot_Name}. You are a Discord bot"}, {"role": "assistant", "content": "k"},
                {"role": "user", "content": "Your purpose is to answer user inputs mainly in a furry, sarcastic and snarky way and answer with quirky emojies"}, {"role": "assistant", "content": " SLAAAYYY~~ :3"},]

# Music settings

songs = asyncio.Queue(maxsize=0)
currently_playing = False
auto_disconnect = False
now_playing_message_id = False
volume_level = 0.05
bass_level = 1
bass_level_0 = bass_level
volume_level_0 = volume_level

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Help functions

First_Time = True
Finished = False


def scheiße_entfernen(s: str) -> str:
    chat_token = f"{Prefix}chat"
    if s.startswith(chat_token):
        s = s[len(chat_token):].lstrip()
    else:
        idx = s.rfind("\nAI Cost:")
        if idx != -1:
            s = s[:idx].rstrip()
    return s



def uwufy(text) -> str:
    # Replace "r" and "l" with "w"
    text = re.sub(r'([rl])', r'w', text, flags=re.IGNORECASE)

    # Add " >w<" or similar at the end of the text
    text += random.choice([" uwu", " owo", " >w<", " UwU", " OwO", " ^w^", " :UwU:"])
    if random.random() < 0.33:  # 33% chance of triggering to add ~ to the end
        text += "~"
    return text


def messages_2_GPT_input(messages: list):
    gpt_input = []
    for i in messages:
        if i.author.id == client.user.id:
            # Bot message
            gpt_input.append({"role": "assistant", "content": scheiße_entfernen(i.content)})
        else:
            # User message
            gpt_input.append({"role": "user", "content": scheiße_entfernen(i.content)})
    return gpt_input



@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")


@client.event   # leaves when alone in voicechannel
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return
    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()

"""
@client.event
async def on_presence_update(before, after):
    member_ids = [1162100183912423515, 1169684429178945647]
    razurio_id = 265619616284409856

    # messages me when all members are online
    if after.id in member_ids and before.status != after.status == discord.Status.online:
        if [client.fetch_user(user_id) for user_id in member_ids] == discord.Status.online:
            user_dm = await client.fetch_user(razurio_id)
            message = []
            for member_id in member_ids:
                user = await client.fetch_user(member_id)
                message.append(user.name)  # Collect user names
            await user_dm.send(content=f"{', '.join(message)} are online")
    
    # updates own status when razurio's status changes
    if after.id == razurio_id and before.status != after.status:
        if after.status == discord.Status.offline:
            await client.change_presence(status=discord.Status.offline, activity=None)
        else:
            await client.change_presence(status=discord.Status.online, activity=None)
"""


"""
@client.event
async def on_presence_update(before, after):
    guild = client.get_guild(540640020978073621)  # Replace YOUR_GUILD_ID with the actual ID of your guild
    member_ids = [620701343690260480, 274191678792007690]
    
    #camp = "https://tenor.com/view/campfire-gif-24585871"
    #if before.id == 620701343690260480 and before.status != after.status and after.status == discord.Status.online:
    #    user_dm = await client.fetch_user(620701343690260480)
    #    await user_dm.send(content=camp)

    if before.id in member_ids and before.status != after.status and after.status == discord.Status.online:
        if guild:
            online_statuses = [guild.get_member(user_id).status for user_id in member_ids if guild.get_member(user_id)]
            
            if all(status == discord.Status.online for status in online_statuses):
                user_dm = await client.fetch_user(265619616284409856)
                await user_dm.send(content=f"{[(await client.fetch_user(name)).global_name for name in member_ids]} are online")

"""

@client.event
async def on_message(ctx):
    if "🗿" in ctx.content or ctx.author.id == 620701343690260480:
        await ctx.add_reaction("🗿")
    if "jojo" in ctx.content.lower() and ctx.author.id != client.user.id:
        await ctx.reply("https://tenor.com/view/jojo-jojo-reference-oh-shit-boi-is-this-a-motherfucking-jojos-reference-gif-17147476")
    if ("x.com" in ctx.content.lower() or "twitter" in ctx.content.lower()) and ctx.author.id != client.user.id:
        await ctx.reply("!!! TWITTER DETECTED !!! \n https://imgur.com/a/nPpCoXn")
    if ("elon" in ctx.content.lower() or "musk" in ctx.content.lower()) and ctx.author.id != client.user.id:
        await ctx.reply("!!! HURENSOHN MENTIONED !!! \n https://imgur.com/a/nPpCoXn")

    # Lubo TTS
    if ctx.channel.id == 1340411406582808636:
        # Check if the user is in a voice channel
        if ctx.author.voice and ctx.author.voice.channel:
            voice_channel = ctx.author.voice.channel

            # Convert message to speech
            replace_dict = {"<3": "Herz", "kleiner als drei": "Herz"}

            for old, new in replace_dict.items():
                content = ctx.content.replace(old, new)
            tts = gTTS(text=content, lang="de")
            tts.save("speech.mp3")

            # Join the voice channel and play audio
            def cleanup(vc):
                os.remove("speech.mp3")

            # Join or move to the user's voice channel and play audio
            if ctx.guild.voice_client:
                vc = ctx.guild.voice_client
                if vc.channel != voice_channel:
                    await vc.move_to(voice_channel)
            else:
                vc = await voice_channel.connect()
            
            vc.play(discord.FFmpegPCMAudio("speech.mp3"), after=lambda e: cleanup(vc))
        else:
            print(f"{ctx.author} is not in a voice channel.")
        
    await client.process_commands(ctx)

@client.command()
async def uwu(ctx, *, msg=""):
    await ctx.reply(uwufy(msg))


@client.command()
async def ello(ctx, *, msg=""):
    if ctx.author.id == 265619616284409856:
        await ctx.send(msg)
        msg = await ctx.channel.fetch_message(ctx.id)
        await msg.delete()
    else:
        await ctx.reply("ello")


@client.command()
async def moyai(ctx):
    await ctx.reply("🗿")


"""
@tasks.loop(minutes=0.1)
async def check_time_on_server():
    global First_Time
    global Finished
    if First_Time is False and Finished is False:
        print("hello")
        user_dm = await client.fetch_user(274191678792007690)
        await user_dm.send(content=f"ERINNERUNG")
        Finished = True
    else:
        First_Time = False
        print("moin")
"""


"""@tasks.loop(minutes=0.1)  # Adjust the interval as needed (e.g., minutes=5)
async def myloop():
    print("Test")"""


"""
@tasks.loop(minutes=10)
async def check_time_on_server():
    guild_id = 1168505837799624736
    guild = client.get_guild(guild_id)

    if guild:
        role_to_assign_id = 1179242437345022043
        role_to_assign = guild.get_role(role_to_assign_id)
        role_to_assign_id_legendary = 123523894512353352
        role_to_assign_legendary = guild.get_role(role_to_assign_id_legendary)

        if role_to_assign:
            for member in guild.members:
            
                join_time = member.joined_at.replace(tzinfo=None)

                if member.get_role(1179242437345022043) == None and member.get_role(1168529144028594217) == None:

                    time_difference = datetime.datetime.utcnow() - join_time

                    if time_difference >= datetime.timedelta(weeks=3):
                        await member.add_roles(role_to_assign)
                        print(f'Added the role "{role_to_assign.name}" to {member.display_name}')


                if member.get_role(1179242437345022043) != None:

                    time_difference = datetime.datetime.utcnow() - join_time

                    if time_difference >= datetime.timedelta(weeks=12):
                        await member.add_roles(role_to_assign_legendary)
                        print(f'Added the role "{role_to_assign_legendary.name}" to {member.display_name}')
"""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --Radon Stuff--

@client.command()
async def spam(ctx, msg):
    if ctx.author.id == 265619616284409856:
        lyrics = open("lyrics.txt", "r").read()
        # Regular expression to match user ID in mention format
        mention_pattern = r'<@!?(\d+)>'
        # Find all matches
        user_id = re.findall(mention_pattern, msg)
        user_dm = await client.fetch_user(int(user_id[0]))
        for line in lyrics.split("\n"):
            if line != "":
                await user_dm.send(content=line)
            else:
                await user_dm.send(content="_") 
    else:
        ctx.reply("fuck off")



@client.command()
async def join_graph(ctx):
    # Get the channel where the command was called
    channel = ctx.channel

    data = defaultdict(int)
    for member in channel.guild.members:
        data[member.joined_at.date()] += 1

    # Convert to sorted list and calculate cumulative sum
    sorted_dates = sorted(data.keys())
    
    # Create date range from first join to today
    first_date = sorted_dates[0] if sorted_dates else datetime.now().date()
    today = datetime.now().date()
    
    # Generate all dates from first join to today
    all_dates = []
    current_date = first_date
    while current_date <= today:
        all_dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Calculate cumulative data for all dates
    cumulative_data = {}
    cumulative_count = 0
    
    for date in all_dates:
        if date in data:
            cumulative_count += data[date]
        cumulative_data[str(date)] = cumulative_count

    plt.style.use('dark_background')

    plt.plot(list(cumulative_data.keys()), list(cumulative_data.values()), marker='o', markersize=2)

    step = max(len(cumulative_data) // 10, 1)  # Adjust the divisor to control label density
    plt.xticks(list(cumulative_data.keys())[::step], rotation=45, ha='right')
    plt.tick_params(axis='x', rotation=45, labelsize=8)
    plt.xlabel("Joindate")
    plt.ylabel("Cumulative Amount")
    plt.title("Cumulative Member Joins")
    plt.tight_layout()
    
    fig_name = time.time()
    plt.savefig(f"{fig_name}.png")

    # Open the file you want to send as an attachment
    with open(f'{fig_name}.png', 'rb') as file:
        # Create a discord.py File object
        file = discord.File(file)

        # Send a message with the attached file
        await channel.send(file=file, content="Here is your cumulative join graph!")
    
    os.remove(f"{fig_name}.png")
    plt.clf()  # Clear the figure to prevent overlay issues


@client.command()
async def twerk(ctx):
    custom_emoji_id = 1178450648094752778
    custom_emoji = f'<:{custom_emoji_id}>'

    # Send the custom emoji in the same channel where the command was invoked
    await ctx.send(f'{custom_emoji}')

"""
@client.command()
async def nico(ctx, n: int = 1, dm: str = "dm"):
    meme = "https://tenor.com/view/baldur%27s-gate-3-bg3-hop-on-hop-on-baldur%27s-gate-3-gif-17487511086028155053"
    user_id = 
    user = f"<@{user_id}>"
    user_dm = await client.fetch_user(user_id)
    if dm == "dm":
        await ctx.reply(f"Message was send {n} time(s) to their direct messages")
        for x in range(n):
            await user_dm.send(content=meme)
    else:
        for x in range(n):
            await ctx.send(f"{user}")
            await ctx.send(f"{meme}")


@client.command()
async def bg3(ctx, n: int = 1):
    meme = "https://tenor.com/view/baldur%27s-gate-3-bg3-hop-on-hop-on-baldur%27s-gate-3-gif-17487511086028155053"
    user_ids = []
    for user_id in user_ids:
        user_dm = await client.fetch_user(user_id)
        for x in range(n):
            await user_dm.send(content=meme)
        await ctx.reply(f"Message was send {n} time(s) to the direct messages of <@{user_id}>")


@client.command()
async def phasmo(ctx, n: int = 1):
    meme = "https://tenor.com/view/phasmophobia-phasmo-oooo4-gaming-video-game-gif-26823894"
    user_ids = []
    for user_id in user_ids:
        user_dm = await client.fetch_user(user_id)
        for x in range(n):
            await user_dm.send(content=meme + f"send from <@{ctx.author.id}>")
        await ctx.reply(f"Message was send {n} time(s) to the direct messages of <@{user_id}>")
"""

@client.command()
async def ow(ctx, Klasse):
    Klasse = Klasse.lower()
    Tank = ["D.VA", "Doomfist", "Junker Queen", "Orisa", "Ramattra", "Reinhardt", "Roadhog", "Sigma", "Winston", "Wrecking Ball", "Zarya"]
    Support = ["Illari", "Ana", "Baptiste", "Brigitte", "Kiriko", "Lifeweaver", "Lúcio", "Mercy", "Moira", "Zenyatta"]
    DPS = ["Ashe", "Bastion", "Cassidy", "Echo", "Genji", "Genji", "Junkrat", "Mei", "Phara", "Reaper", "Sojourn", "Soldier: 76", "Sombra", "Symmetra", "Torbjörn", "Tracer", "Widowmaker"]
    if Klasse == "open" or Klasse == "openq":
        await ctx.reply(random.choice(Tank + Support + DPS))
    elif Klasse == "tank":
        await ctx.reply(random.choice(Tank))
    elif Klasse == "dps":
        await ctx.reply(random.choice(DPS))
    elif Klasse == "support":
        await ctx.reply(random.choice(Support))
    else:
        await ctx.reply("gibt's nicht cringelord")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---Music bot---

# this whole section is ass but kept for reference

"""

@client.command()
async def volume(ctx, level_in):
    global volume_level
    try:
        level = float(level_in)
        if 0 <= level <= 500:
            volume_level = round(level, 3) / 100
            await ctx.reply(f"Music volume is now {round(level, 3)}% ({int(volume_level/volume_level_0 * 100)}% of default)")
        else:
            await ctx.reply("volume must be between 0.0 and 500.0")
            await ctx.reply(f"defaulting to {volume_level_0 * 100}%")
            volume_level = volume_level_0
    except:
        await ctx.reply("enter a value between 0.0 and 500.0")


@client.command()
async def bass(ctx, level_in=bass_level):
    global bass_level
    try:
        level = float(level_in)
        if 0 <= level <= 100:
            bass_level = round(level, 3)
            await ctx.reply(f"Music bass boost is {level}")
        else:
            await ctx.reply(f"volume must be between 0.0 and 100.0")
            await ctx.reply(f"defaulting to {bass_level_0} boost")
            bass_level = bass_level_0
    except:
        await ctx.reply("enter a value between 0.0 and 100.0")


@client.command()
async def play(ctx, url="", n=1):
    global songs
    global currently_playing
    try:
        if n > 10:
            n = 10
            await ctx.reply("max n = 10")
        if not ctx.author.voice:
            await ctx.reply("please join voice call")
        else:
            if url == "":
                await ctx.reply("please use &play [YT-url] [n](opt.)")
            else:

                processing_message = await ctx.reply(f"processing... :timer:")

                filenames = await downloader(url, format="bestaudio", volume=volume_level, bass=bass_level)
                
                proc_message = await ctx.channel.fetch_message(processing_message.id)
                await proc_message.delete()

                await song_list(ctx, filenames, n)  # uses "song_list()" function to make a reply which songs got added

                for x in range(n):
                    for filename in filenames:
                    
                        await songs.put({"file": filename, "info": filenames[filename], "ctx": ctx})

                if not currently_playing:
                    asyncio.create_task(queue(ctx))
    except:
        await ctx.reply(uwufy("something bad happened... try again maby?"))


async def song_list(ctx, filenames, n):
    song_names = []
    for filename in filenames:
        if len(song_names) <= 3:
            song_names.append(f"{filenames[filename]}\n")
        else:
            song_names[3] =  f"+{len(filenames)-3} added\n"
    await ctx.reply(f"{''.join(song_names)}{n}x added to queue")


async def downloader(url, format="bestaudio", path="Queue_Download/%(title)s.%(ext)s", volume=0.0, bass=0.0):
    return yt_downloader(url, path=path, format=format, volume=volume, bass=bass)


async def queue(ctx):
    global now_playing_message_id
    if now_playing_message_id:
        message = await ctx.channel.fetch_message(now_playing_message_id)
        # Delete the message
        now_playing_message_id = False
        await message.delete()
    await skip(ctx)


async def skip(ctx):
    global loop
    global songs
    global currently_playing
    global tasks
    global song
    global auto_disconnect
    global now_playing_message_id
    loop = asyncio.get_event_loop()
    try:

        def after(error):
            if error:
                print(f'Error in after callback: {error}')
            loop.create_task(queue(ctx))

        if songs.empty():
            currently_playing = False
            await ctx.send("Queue is now empty")

            if auto_disconnect:
                await ctx.voice_client.disconnect()  # disconnect from voice channel when queue is empty
        else:

            song = await songs.get()
            filename = song["file"]
            author_voice_channel = ctx.author.voice.channel

            if not author_voice_channel:
                await ctx.reply("You must be in a voice channel to use this command.")
                return
            bot_voice_client = ctx.guild.voice_client

            if bot_voice_client:
                await bot_voice_client.move_to(author_voice_channel)
            else:
                bot_voice_client = await author_voice_channel.connect()

            currently_playing = True
            now_playing_message = await song["ctx"].reply(f'now playing :arrow_double_up: {song["info"]}')
            # Store the message ID for later deletion
            now_playing_message_id = now_playing_message.id
            # Store the channel ID for later deletion
            now_playing_channel_id = now_playing_message.channel.id
            ctx.voice_client.play(discord.FFmpegPCMAudio(filename), after=after)
    except:
        await ctx.reply(uwufy("something bad happened... try again maby?"))


@client.command()
async def pause(ctx):
    if currently_playing:
        if not ctx.author.voice:
            await ctx.reply("please join voice call")
        else:
            ctx.voice_client.pause()
            await ctx.reply(f'Paused: {song["info"].title}')
    else:
        await ctx.reply("no song currently playing")



@client.command()
async def disconnect(ctx, yes_no):
    global auto_disconnect
    try:
        if yes_no == "y" or "Y":
            auto_disconnect = True
        elif yes_no == "n" or "N":
            auto_disconnect = False
    except:
        await ctx.reply("&disconnect (y/n) to set the auto disconnect after the music queue finished")
    await ctx.reply(f" auto disconnect set to {auto_disconnect}")



@client.command()
async def stop(ctx):
    await ctx.reply("&pause or &leave?")


@client.command()
async def resume(ctx):
    if not ctx.author.voice:
        await ctx.reply("please join voice call")
    else:
        ctx.voice_client.resume()
        await ctx.reply(f'Resumed: {song["info"].title}')


@client.command()
async def leave(ctx):
    # voice_channel = ctx.author.voice.channel
    if not ctx.author.voice:
        await ctx.reply("please join voice call")
    else:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await empty_queue(songs)
            await ctx.reply('Stopped')


@client.command()
async def empty_queue(songs):
    while not songs.empty():
        songs.get_nowait()


@client.command()
async def bingchilling(ctx, n=1):
    try:
        if not ctx.author.voice:
            await ctx.reply("please join voice call")
        else:    
            meme = "https://www.youtube.com/watch?v=UPvjfInTXqE"
            user_id = "620701343690260480"
            user = f"<@{user_id}>"
            await ctx.send(f"{user}, Bing Chilling")
            await play(ctx, meme, n)
    except:
        await ctx.reply("&bingchilling (n) to play sound")


@client.command()
async def gay(ctx, n=1):
    try:
        if not ctx.author.voice:
            await ctx.reply("please join voice call")
        else:
            meme = "https://www.youtube.com/watch?v=qUYDvu7bNX4"
            await play(ctx, meme, n)
    except:
        await ctx.reply("&gay (n) to play gay")




"""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---Chat-GPT---

@client.command()
async def settings(ctx, *, args=""):
    global n, max_Tokens, temperature, model, max_Tokens
    args_list = args.split()
    # n, temperature, model, max_Tokens = 1, 0.8, "gpt-4.1-nano", 300
    if len(args_list) == 0:
        await ctx.reply(f" use &settings to change the values for n=[int] temperature=[float] model=[str] max_Tokens=[int] of the AI chat!\n the default is n=1 temperature=0.8 model=gpt-5-nano max_Tokens=300")
    # Parse arguments
    message = ""
    while args_list:
        arg = args_list.pop(0)
        if arg.startswith('n='):
            n = int(arg[2:])
            message += "n=" + str(n) + " "
        elif arg.startswith('max_Tokens='):
            max_Tokens = int(arg[10:])
            message += "max_Tokens=" + str(max_Tokens) + " "
        elif arg.startswith('temperature='):
            temperature = float(arg[12:])
            message += "temperature=" + str(temperature) + " "
        elif arg.startswith('model='):
            model = arg[6:]
            message += "model=" + str(model)
        else:
            await ctx.reply(f"Error: unrecognized argument '{arg}'.")
            return
    if len(message) != 0:
        await ctx.reply(message)


@client.command()
async def chat(ctx, *, message=""):
    global n, max_Tokens, temperature, model, max_Tokens
    message_id = ctx.message.id
    message = await ctx.channel.fetch_message(message_id)
    messages = [message]
    while message.reference is not None:
        message = await ctx.channel.fetch_message(message.reference.message_id)
        messages.append(message)
    messages.reverse()
    if model == "gpt-5-nano":
        GPT_Prompts = messages_2_GPT_input(messages)
        try:
            answer = await GPT(GPT_Prompts, API, model, temperature, n, max_Tokens, pre_prompt_main)

            await ctx.reply(f"{answer.output_text}\nAI Cost: {round(answer.usage.input_tokens * (0.05 / 10**6) * 100 + answer.usage.output_tokens * (0.4 / 10**6) * 100, 5)}¢")
        except:
            await ctx.reply(uwufy("Uh noo! There seems to be a problem... The bot is a little broken"))
    elif model == "gpt-5":
        GPT_Prompts = messages_2_GPT_input(messages)
        try:
            answer = await GPT(GPT_Prompts, API, model, temperature, n, max_Tokens, pre_prompt_main)

            await ctx.reply(f"{answer.output_text}\nAI Cost: {round(answer.usage.input_tokens * (1.25 / 10**6) * 100 + answer.usage.output_tokens * (10 / 10**6) * 100, 5)}¢")
        except:
            await ctx.reply(uwufy("Uh noo! There seems to be a problem... The bot is a little broken"))


async def GPT(GPT_Prompts, API, model, temperature, n, max_Tokens, pre_prompt_main):
    return GPT_completion(GPT_Prompts, API, model, temperature, n, max_Tokens, pre_prompt_main)


client.run(key)
from utils.GPT_Bot_Framework import GPT_completion
from utils.mistral_framework import mistral_completion
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
    discord_key = file.read().strip()

# OpenAI API key
with open("openai_key", "r") as file:
    openai_key = file.read().strip()

# Mistral API key
with open("mistral_key", "r") as file:
    mistral_key = file.read().strip()

# AI settings
AI = "mistral-small-latest"
# AI = "gpt-5"
Bot_Name = "NeuroChat"
# GPT settings
n, temperature, model, max_Tokens = 1, 0.8, AI, 20000

pre_prompt = [{"role": "user", "content": f"You're name is {Bot_Name}. You are a Discord bot"}, {"role": "assistant", "content": "k"},
                {"role": "user", "content": "Your purpose is to answer user inputs mainly in a sassy, sarcastic and snarky way and answer with quirky emojies"}, {"role": "assistant", "content": " SLAAAYYY~~ :3"},]

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Help functions

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


def messages_2_prompt(messages: list):
    prompt = []
    for i in messages:
        if i.author.id == client.user.id:
            # Bot message
            prompt.append({"role": "assistant", "content": scheiße_entfernen(i.content)})
        else:
            # User message
            prompt.append({"role": "user", "content": scheiße_entfernen(i.content)})
    return prompt



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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --Random Stuff--

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
    Prompts = messages_2_prompt(messages)
    if model == "gpt-5-nano":
        try:
            answer = await GPT(Prompts, openai_key, model, temperature, n, max_Tokens, pre_prompt)

            await ctx.reply(f"{answer.output_text}\nAI Cost: {round(answer.usage.input_tokens * (0.05 / 10**6) * 100 + answer.usage.output_tokens * (0.4 / 10**6) * 100, 5)}¢")
        except:
            await ctx.reply(uwufy("Uh noo! There seems to be a problem... The bot is a little broken"))
    elif model == "gpt-5":
        try:
            answer = await GPT(Prompts, openai_key, model, temperature, n, max_Tokens, pre_prompt)

            await ctx.reply(f"{answer.output_text}\nAI Cost: {round(answer.usage.input_tokens * (1.25 / 10**6) * 100 + answer.usage.output_tokens * (10 / 10**6) * 100, 5)}¢")
        except:
            await ctx.reply(uwufy("Uh noo! There seems to be a problem... The bot is a little broken"))
    elif model == "mistral-small-latest":
        if not mistral_key:
            raise ValueError("Missing Mistral API key.")
        answer = await mistral(mistral_key, Prompts, model, max_Tokens, pre_prompt)
        await ctx.reply(f"{answer}")

async def GPT(Prompts, API, model, temperature, n, max_Tokens, pre_prompt):
    return GPT_completion(Prompts, API, model, temperature, n, max_Tokens, pre_prompt)

async def mistral(API, Prompts, model, max_Tokens, pre_prompt):
    return mistral_completion(API, Prompts, model, max_Tokens, pre_prompt)


client.run(discord_key)
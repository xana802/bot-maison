import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import discord, os , asyncio
load_dotenv()

print ('initialisation bot devastra')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def load():
     for file in os.listdir("./commande"):
        if file.endswith(".py"):
            await bot.load_extension(f"commande.{file[:-3]}")

@bot.event
async def on_ready():
    print("Bot intialise")
    # syncroniser les commades    
    try:
        #sync
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées: " + str(len(synced)))
    except Exception as e :
        print(e)
@bot.event
async def on_message(message: discord.Message):
    #empeche le bot de se repondre a lui meme
    if message.author.bot:
        return
    if message.content.lower() == 'bonjour':
        chanel = message.channel
        await chanel.send('laisse moi dormir chacal')

   
@bot.tree.command(name="dodo", description="juste dodo")
async def dodo(message: discord.Message):
    await message.response.send_message("faut dormir la nuit ! 😴")

async def main():
    async with bot:
        await load()
        await bot.start(os.getenv("Discord_token"))
        
asyncio.run(main())
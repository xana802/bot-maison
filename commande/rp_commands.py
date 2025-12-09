import discord
import os
import datetime
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

CATEGORY_LOG_FOLDERS = {
    int(os.getenv("CHANDRA_CAT")): os.getenv("CHANDRA_FOLDER"),
    int(os.getenv("GARUDA_CAT")): os.getenv("GARUDA_FOLDER"),
    int(os.getenv("JEUX_CAT")): os.getenv("JEUX_FOLDER"),
    int(os.getenv("KALI_CAT")): os.getenv("KALI_FOLDER"),
    int(os.getenv("KAMA_CAT")): os.getenv("KAMA_FOLDER"),
    int(os.getenv("YAMA_CAT")): os.getenv("YAMA_FOLDER")
}

def save_message(message: discord.Message, folder: str):
    if not os.path.exists(folder):
        print(f"⚠️ Le dossier '{folder}' n'existe pas. Message ignoré.")
        return

    filename = os.path.join(folder, f"channel_{message.channel.id}.txt")
    time = datetime.datetime.now().strftime("[%d/%m/%Y %H:%M]")

    with open(filename, "a", encoding="utf-8") as f:
        author = f"{message.author.display_name}#{message.author.discriminator}"
        f.write(f"{time} {author}: {message.content}\n")


class rpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rp_active = False

    @app_commands.command(name="rp_on", description="Active la phase RP")
    async def rp_on(self, interaction: discord.Interaction):
        if self.rp_active:
            msg = "La phase RP est déjà activée !"
        else:
            msg = "🎭 La phase RP est maintenant activée !"
            self.rp_active = True
        await interaction.response.send_message(msg)

    @app_commands.command(name="rp_off", description="Désactive la phase RP")
    async def rp_off(self, interaction: discord.Interaction):
        if not self.rp_active:
            msg = "La phase RP est déjà désactivée !"
        else:
            msg = "🚫 La phase RP est maintenant désactivée !"
            self.rp_active = False
        await interaction.response.send_message(msg)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # Si RP actif, on sauvegarde
        if self.rp_active:
            folder = CATEGORY_LOG_FOLDERS.get(message.channel.category_id)
            if folder:
                save_message(message, folder)
                print(f"Message sauvegardé dans '{folder}' (channel {message.channel.id})")

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(rpCommands(bot))
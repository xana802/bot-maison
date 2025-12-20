import discord
import os
import json
import datetime
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
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
        print(f"⚠️ Dossier inexistant : {folder}")
        return

    filename = os.path.join(folder, f"channel_{message.channel.id}.json")

    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "author": f"{message.author.display_name}#{message.author.discriminator}",
        "content": message.content
    }

    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []
    else:
        data = []

    data.append(log_entry)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class RP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rp_active = False  # LA SEULE VARIABLE RP

        # Charge les catégories depuis env
        from dotenv import dotenv_values
        env = dotenv_values(".env")

        global CATEGORY_LOG_FOLDERS
        CATEGORY_LOG_FOLDERS = {
            int(env["CHANDRA_CAT"]): env["CHANDRA_FOLDER"],
            int(env["GARUDA_CAT"]): env["GARUDA_FOLDER"],
            int(env["JEUX_CAT"]): env["JEUX_FOLDER"],
            int(env["KALI_CAT"]): env["KALI_FOLDER"],
            int(env["KAMA_CAT"]): env["KAMA_FOLDER"],
            int(env["YAMA_CAT"]): env["YAMA_FOLDER"]
        }

    # -----------------------------
    # COMMANDES SLASH
    # -----------------------------
    @app_commands.command(name="rp_on", description="Active le mode RP")
    async def rp_on(self, interaction: discord.Interaction):
        self.rp_active = True
        await interaction.response.send_message("🎭 Mode RP ACTIVÉ")
        print("=== MODE RP ACTIVÉ ===")

    @app_commands.command(name="rp_off", description="Désactive le mode RP")
    async def rp_off(self, interaction: discord.Interaction):
        self.rp_active = False
        await interaction.response.send_message("🚫 Mode RP DÉSACTIVÉ")
        print("=== MODE RP DÉSACTIVÉ ===")

    # -----------------------------
    # LISTENER RP
    # -----------------------------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if not self.rp_active:
            return

        folder = CATEGORY_LOG_FOLDERS.get(message.channel.category_id)

        if folder:
            save_message(message, folder)
            print(f"[LOG] Message sauvegardé -> {folder} / channel {message.channel.id}")

async def setup(bot):
    await bot.add_cog(RP(bot))
import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DATA_FOLDER = "log_serv"
DATA_FILE = "log_serv/persos.json"

# ---------- UTILS ----------
def load_data():
    if not os.path.exists(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------- MODAL ----------
class PersoModal(discord.ui.Modal, title="Création du personnage"):

    nom = discord.ui.TextInput(
        label="Nom du personnage",
        placeholder="Ex : Kael Limbo Geko",
        max_length=30
    )

    race = discord.ui.TextInput(
        label="Race",
        placeholder="Choisis ta race",
        max_length=50
    )

    classe = discord.ui.TextInput(
        label="Classe",
        placeholder="Choisis ta classe",
        max_length=50
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        data = load_data()
        user_id = str(interaction.user.id)

        perso = {
            "nom": self.nom.value,
            "race": self.race.value,
            "classe": self.classe.value,
            "serveur_id": str(interaction.guild.id),
            "created_at": discord.utils.utcnow().strftime("%Y-%m-%d %H:%M")
        }

        if user_id not in data:
            data[user_id] = []

        data[user_id].append(perso)
        save_data(data)

        embed = discord.Embed(
            title="📜 PERSONNAGE",
            color=discord.Color.gold()
        )
        embed.add_field(name="Nom", value=perso["nom"], inline=False)
        embed.add_field(name="Race", value=perso["race"], inline=True)
        embed.add_field(name="Classe", value=perso["classe"], inline=True)
        embed.set_footer(text=f"Joué par {interaction.user.display_name}")

        log_guild = interaction.client.get_guild(int(os.getenv("LOG_GUILD_ID")))
        log_channel = log_guild.get_channel(int(os.getenv("LOG_CHANNEL_ID")))

        if log_channel:
            await log_channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ Ton personnage a été enregistré avec succès.",
            ephemeral=True
        )

# ---------- BOUTON ----------
class ValiderButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Créer", style=discord.ButtonStyle.blurple)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            PersoModal(interaction.client)
        )

# ---------- VIEW ----------
class CreationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(ValiderButton())

# ---------- COG ----------
class CreationPerso(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.temp_perso = {}

    @app_commands.command(
        name="creation_perso",
        description="Créer un personnage (nom, race et classe libres)"
    )
    async def creation_perso(self, interaction: discord.Interaction):
        self.bot.temp_perso[interaction.user.id] = {}

        embed = discord.Embed(
            title="🧙 Création de personnage",
            description=(
                "Clique sur **Créer** pour créer ton personnage.\n\n"
                "Tu pourras renseigner :\n"
                "• Nom\n"
                "• Race\n"
                "• Classe"
            ),
            color=discord.Color.purple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=CreationView(),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(CreationPerso(bot))
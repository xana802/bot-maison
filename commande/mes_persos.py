import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DATA_FILE = "log_serv/persos.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- SELECT ----------
class PersoSelect(discord.ui.Select):
    def __init__(self, persos):
        options = [
            discord.SelectOption(label=p["nom"], description=f"{p['race']} • {p['classe']}")
            for p in persos
        ]
        super().__init__(
            placeholder="Choisis un personnage à afficher",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        data = load_data()
        user_id = str(interaction.user.id)

        perso = next(
            p for p in data[user_id] if p["nom"] == self.values[0]
        )

        embed = discord.Embed(
            title=f"📜 Fiche de {perso['nom']}",
            color=discord.Color.gold()
        )
        embed.add_field(name="🧬 Race", value=perso["race"], inline=True)
        embed.add_field(name="⚔️ Classe", value=perso["classe"], inline=True)
        embed.set_footer(text=f"Joué par {interaction.user.display_name}")

        # ➜ Message PUBLIC dans le salon
        await interaction.channel.send(embed=embed)

# ---------- VIEW ----------
class PersoView(discord.ui.View):
    def __init__(self, persos):
        super().__init__(timeout=120)
        self.add_item(PersoSelect(persos))

# ---------- COG ----------
class MesPersonnages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="mes_personnages",
        description="Afficher ton personnages"
    )
    async def mes_personnages(self, interaction: discord.Interaction):
        data = load_data()
        user_id = str(interaction.user.id)

        if user_id not in data or not data[user_id]:
            await interaction.response.send_message(
                "❌ Tu n'as aucun personnage.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📜 Tes personnages",
            description="Sélectionne un personnage à afficher publiquement",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=PersoView(data[user_id]),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(MesPersonnages(bot))
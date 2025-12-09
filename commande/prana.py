import discord
from discord import app_commands
from discord.ext import commands
import json
import os

# Charger les données de prana
if os.path.exists("prana.json"):
    with open("prana.json", "r") as f:
        prana_data = json.load(f)
else:
    prana_data = {}

def save_prana():
    with open("prana.json", "w") as f:
        json.dump(prana_data, f, indent=4)

class prana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commande pour afficher le prana
    @app_commands.command(name="prana", description="Affiche l'état de prana d'un personnage")
    @app_commands.describe(pseudo="Nom du personnage")
    async def sante(self, interaction: discord.Interaction, pseudo: str):
        if pseudo in prana_data:
            prana = prana_data[pseudo]["prana"]
            prana_max = prana_data[pseudo]["prana_max"]
        else:
            await interaction.response.send_message(f"{pseudo} n'a pas de prana défini.")
            return

        barre = int((prana / prana_max) * 10)
        bar_graph = "🟥" * barre + "⬛" * (10 - barre)

        embed = discord.Embed(
            title=f"Prana de {pseudo}",
            description=f"{bar_graph}\n**{prana} / {prana_max} PV**",
            color=discord.Color.red()
        )
        embed.set_author(name=pseudo)

        await interaction.response.send_message(embed=embed)

    # Commande pour définir le prana
    @app_commands.command(name="set_prana", description="Définit le prana d'un personnage")
    @app_commands.describe(pseudo="Nom du personnage", prana="Prana actuel", prana_max="Prana maximum")
    async def set_prana(self, interaction: discord.Interaction, pseudo: str, prana: int, prana_max: int):
        if prana > prana_max:
            prana = prana_max
        prana_data[pseudo] = {"prana": prana, "prana_max": prana_max}
        save_prana()
        await interaction.response.send_message(f"Prana de {pseudo} défini à {prana}/{prana_max}.")

    # Commande pour ajouter ou retirer du prana
    @app_commands.command(name="add_prana", description="Ajoute ou retire du prana à un personnage")
    @app_commands.describe(pseudo="Nom du personnage", amount="Nombre de prana à ajouter (ou retirer avec un nombre négatif)")
    async def add_prana(self, interaction: discord.Interaction, pseudo: str, amount: int):
        if pseudo not in prana_data:
            await interaction.response.send_message(f"{pseudo} n'a pas de prana défini.")
            return

        prana_data[pseudo]["prana"] += amount
        # Vérifier limites
        if prana_data[pseudo]["prana"] > prana_data[pseudo]["prana_max"]:
            prana_data[pseudo]["prana"] = prana_data[pseudo]["prana_max"]
        elif prana_data[pseudo]["prana"] < 0:
            prana_data[pseudo]["prana"] = 0

        save_prana()
        await interaction.response.send_message(
            f"Prana de {pseudo} mis à jour : {prana_data[pseudo]['prana']}/{prana_data[pseudo]['prana_max']}."
        )

async def setup(bot):
    await bot.add_cog(prana(bot))
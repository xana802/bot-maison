import discord
import json
import os
from discord.ext import commands

WALLET_FILE = "wallets.json"

def read_wallets():
    if not os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "w") as f:
            f.write("{}")
    with open(WALLET_FILE, "r") as f:
        return json.load(f)

def write_wallets(data):
    with open(WALLET_FILE, "w") as f:
        json.dump(data, f, indent=4)

class wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="wallet", description="Affiche ton argent")
    async def wallet(self, interaction: discord.Interaction):
        data = read_wallets()
        user_id = str(interaction.user.id)

        # Donne 0 si l'utilisateur n'est pas dans le fichier
        wallet = data.get(user_id, 0)

        await interaction.response.send_message(
            f"💰 **{interaction.user.name}, tu as `{wallet}` pièces.**"
        )

    @discord.app_commands.command(name="addmoney", description="Ajoute de l'argent (admin)")
    async def addmoney(self, interaction: discord.Interaction, montant: int, utilisateur: discord.Member):
        # Sécurité : réservé admins
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⛔ Tu n'as pas la permission !")
            return

        data = read_wallets()
        user_id = str(utilisateur.id)

        if user_id not in data:
            data[user_id] = 0

        data[user_id] += montant
        write_wallets(data)

        await interaction.response.send_message(
            f"🏦 `{montant}` pièces ajoutées à **{utilisateur.name}**"
        )

    @discord.app_commands.command(name="setwallet", description="Définit l'argent d'un joueur (admin)")
    async def setwallet(self, interaction: discord.Interaction, montant: int, utilisateur: discord.Member):
            await interaction.response.defer()  # réponse différée
            # Vérification permissions admin
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("⛔ Tu n'as pas la permission !")
                return
            
            # Lire les données
            data = read_wallets()
            user_id = str(utilisateur.id)

            # Écraser la valeur
            data[user_id] = montant
            write_wallets(data)

            await interaction.response.send_message(
                f"💼 Le portefeuille de **{utilisateur.name}** est maintenant à **{montant} pièces.**"
            )

async def setup(bot):
    await bot.add_cog(wallet(bot))
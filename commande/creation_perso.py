from discord.ext import commands
import discord
from discord import app_commands

class creation_perssonage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="creation_perso", description="creation perso dans un embed")
    @app_commands.describe(pseudo="Pseudo du personnage", texte="toute lhistoire de ton perso")
    async def creation_perso(self,interaction: discord.Interaction, pseudo: str, texte: str):
        await interaction.response.defer()  # réponse différée
        embed = discord.Embed(
            title="📜 fiche perssonage 📜",
            description=f"**pour {pseudo}** \n {texte}",
            color=0xFFD700
        )
        embed.set_author(name=pseudo)
            
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(creation_perssonage(bot))
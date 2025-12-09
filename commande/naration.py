from discord.ext import commands
import discord
from discord import app_commands

class Naration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="naration", description="Affiche la narration dans un embed")
    @app_commands.describe(pseudo="Pseudo du personnage", texte="Texte de la narration")
    async def naration(self,interaction: discord.Interaction, pseudo: str, texte: str):
        await interaction.response.defer()  # réponse différée
        embed = discord.Embed(
            title="📜 Narration 📜",
            description=f"**pour {pseudo}** \n {texte}",
            color=0xFFD700
        )
        embed.set_author(name=pseudo)
            
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Naration(bot))
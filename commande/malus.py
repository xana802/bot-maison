import discord
from discord.ext import commands 
import random

class Malus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="malus", description="come le /lance mais pour les malus")
    async def malus(self,interaction, nombre: int, face: int = 20):
        n=nombre
        f=face
        if n <= 0 or f <= 1:
            await interaction.response.send_message("Nombre invalide !")
            return

        resultats = [random.randint(1, f) for _ in range(n)]
        total = sum(resultats)
        
        # Commentaire selon le total
        if total == n * f * 1:  # Tous les dés montrent 1
            commentaire = "surment de legeres egratibures"
        elif total >= n * f * 0.9: # 90% du max
            commentaire = "surement de legeres blessures"
        elif total >= n * f * 0.8:  # 80% du maximum
            commentaire = "des blessures modérées"
        elif total >= n * f * 0.6:  # 60% du max
            commentaire = "les blessures commence a etre serieuse"
        elif total >= n * f * 0.5:  # 50% du max
            commentaire = "sa sens mauvais cette histoire"
        elif total <= n * f * 0.49:  # 40% du max
            commentaire = "sa comence a piquer severe"
        elif total <= n * f * 0.3:  # 30% du max
            commentaire = "franchement mal en point la"
        elif total <= n * f * 0.05:  # 0.1% du max
            commentaire = "plus bas tu meurt"


        await interaction.response.send_message(f"{commentaire}\n🎲 **{n} dés à {f} faces :** **{resultats}**\n🔢 **Total :** **{total} ")
        
async def setup(bot):
    await bot.add_cog(Malus(bot))
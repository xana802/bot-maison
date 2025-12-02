from discord.ext import commands
import discord
import random

class Lance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="lance", description="lance les dés avec un nombre de faces personnalisé")
    async def lance(self,interaction, nombre: int, face: int = 6):
        n=nombre
        f=face
        if n <= 0 or f <= 1:
            await interaction.response.send_message("Nombre invalide !")
            return

        resultats = [random.randint(1, f) for _ in range(n)]
        total = sum(resultats)
        
        # Commentaire selon le total
        if total == n * f * 1:  # Tous les dés montrent 1
            commentaire = "😤 **sa sent le cheat a plein nez la faut ce calmer"
        elif total >= n * f * 0.9: # 90% du max
            commentaire = "😎 **le scenar est avec toi ont dirait"
        elif total >= n * f * 0.8:  # 80% du maximum
            commentaire = "🔥 **Excellent score !"
        elif total >= n * f * 0.6:  # 60% du max
            commentaire = "😐 **on va dire sa passe"
        elif total >= n * f * 0.5:  # 50% du max
            commentaire = "🙂 **ta la moyen au moin"
        elif total <= n * f * 0.49:  # 40% du max
            commentaire = "😕 **faut pas plus bas quoi"
        elif total <= n * f * 0.3:  # 30% du max
            commentaire = "💀 **Très faible… Tu as la poisse !"
        elif total <= n * f * 0.01:  # 0.1% du max
            commentaire = "😞 **lache l'affaire"


        await interaction.response.send_message(f"🎲 **{n} dés à {f} faces :** **{resultats}**\n🔢 **Total :** **{total}\n {commentaire}")

async def setup(bot):
    await bot.add_cog(Lance(bot))
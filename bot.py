import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
print("DISCORD_TOKEN présent :", os.getenv("DISCORD_TOKEN") is not None)
print("GUILD_ID présent :", os.getenv("GUILD_ID") is not None)
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="ping", description="Teste si le bot répond", guild=GUILD)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Hey ! On m'a appelé ? Pour plus d'aide n'hésites pas à employer la commande /help ! ^^")


@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    print(f"Connecté en tant que {client.user}")


client.run(TOKEN)
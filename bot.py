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

@tree.command(name="serveurinfo", description="Informations sur le serveur", guild=GUILD)
async def serveurinfo(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(title=guild.name,description="Voici les infos sur le serveur !",
                          color=discord.Color(0x5865F2),
                          timestamp=discord.utils.utcnow(),
                          )
    embed.add_field(name="👥 Membres", value=guild.member_count)
    embed.add_field(name="Créé le", value="Juin 2022")
    embed.add_field(name="Propriétaire", value=".riyo_")
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=f"Demandé par {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed)

@tree.command(name="userinfo",description="Information sur l'utilisateur recherché",guild=GUILD)
@app_commands.describe(member="Le membre à inspecter")
async def userinfo(interaction : discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=member.display_name, color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="🆔 Identifiant", value=member.id)
    embed.add_field(name="📅 Compte créé le", value=discord.utils.format_dt(member.created_at, "D"))
    if member.joined_at:
        embed.add_field(name="📥 A rejoint le", value=discord.utils.format_dt(member.joined_at, "D"))
    roles = ""
    for role in member.roles[1:]:
        roles = roles + role.mention + " "
    if roles == "":
        roles = "Aucun rôle"
    embed.add_field(name="🎭 Rôles", value=roles)
    
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    print(f"Connecté en tant que {client.user}")


client.run(TOKEN)
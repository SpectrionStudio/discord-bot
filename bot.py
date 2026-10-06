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
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="ping", description="Ping le bot pour lui parler", guild=GUILD)
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
async def userinfo(interaction : discord.Interaction, member: discord.Member | None = None):
    if member is None:
        member = interaction.user
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

@tree.command(name="help", description="Toutes les commandes que je peux exécuter !", guild=GUILD)
async def help_command(Interaction : discord.Interaction):
    embed = discord.Embed(title="Commandes du bot discord", color=discord.Color(0x5865F2))

    for commande in tree.get_commands(guild=GUILD):
        embed.add_field(name=f"/{commande.name}", value=commande.description, inline=False)
    await Interaction.response.send_message(embed=embed)


@tree.command(name="linktree", description="Obtenez tous nos réseaux grâce à cette commande !", guild=GUILD)
async def linktree(interaction: discord.Interaction):
    embed= discord.Embed(
        title="Retrouvez-nous partout !",
        description="Tous les liens du projet au même endroit !",
        color= discord.Color(0x5865F2),
    )
    embed.add_field(name="📸 Instagram", value="[Notre actualité sur Instagram !](https://www.instagram.com/spectrion_studio)", inline=False)
    embed.add_field(name="🎶 TikTok", value="[Suivez-nous sur Tiktok !](https://www.tiktok.com/@spectrionstudio)", inline=False)
    embed.add_field(name="▶️ YouTube", value="[Notre chaîne Youtube](https://www.youtube.com/@SpectrionStudio)", inline=False)
    embed.add_field(name="🐦 X", value="[Voici notre compte X](https://x.com/spectrionstudio)", inline=False)
    embed.add_field(name="📞 WhatsApp", value="[Besoin de nous contacter ?](https://api.whatsapp.com/send/?phone=33612541310&text&type=phone_number&app_absent=0)", inline=False)
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    print(f"Connecté en tant que {client.user}")

@client.event
async def on_member_join(member):
    channel= member.guild.system_channel
    if channel is None:
        return

    embed = discord.Embed(
        title=f"Bienvenue {member.display_name} !",
        description="Tu es arrivé sur le projet The Release Of Riyo, un serveur discord suivant l'histoire de la création d'un projet Light Novel/Webtoon/Manga en cours de développement !",
        color=discord.Color(0x5865F2),
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Tu es le membre n°{member.guild.member_count}")

    file = discord.File("images/bienvenue.png", filename="bienvenue.png")
    embed.set_image(url="attachment://bienvenue.png")

    await channel.send(content=member.mention, embed=embed, file=file)
client.run(TOKEN)
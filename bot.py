import os
import discord
import datetime
from ia import demander, PROMPT_ASSISTANT, PROMPT_ROMAN, LORE
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
    if interaction.guild.icon:
      embed.set_thumbnail(url=interaction.guild.icon.url)
    embed.add_field(name="📸 Instagram", value="[Notre actualité sur Instagram !](https://www.instagram.com/spectrion_studio)", inline=False)
    embed.add_field(name="🎶 TikTok", value="[Suivez-nous sur Tiktok !](https://www.tiktok.com/@spectrionstudio)", inline=False)
    embed.add_field(name="▶️ YouTube", value="[Notre chaîne Youtube](https://www.youtube.com/@SpectrionStudio)", inline=False)
    embed.add_field(name="🐦 X", value="[Voici notre compte X](https://x.com/spectrionstudio)", inline=False)
    embed.add_field(name="📞 WhatsApp", value="[Besoin de nous contacter ?](https://api.whatsapp.com/send/?phone=33612541310&text&type=phone_number&app_absent=0)", inline=False)
    
    await interaction.response.send_message(embed=embed)

@tree.command(name="clear", description="Permet de supprimer un nombre déterminé de messages", guild=GUILD)
@app_commands.describe(nombre="Nombre de messages à supprimer (1 à 100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, nombre: app_commands.Range[int, 1, 100]) :
    await interaction.response.defer(ephemeral=True)
    supprimes = await interaction.channel.purge(limit=nombre)
    await interaction.followup.send(f"J'ai bien supprimé les {len (supprimes)} messages comme vous me l'avez demandé pour ce salon !" ,ephemeral=True)

@clear.error
async def clear_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Vous ne possédez pas les permissions pour employer cette commande, désolé !", ephemeral=True)
    else:
        print(error)



@tree.command(name="kick", description="Expulser un membre du serveur", guild=GUILD)
@app_commands.describe(member="Le membre à expulser", reason="La raison de son expulsion")
@app_commands.checks.has_permissions(kick_members=True)
@app_commands.checks.bot_has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison fournie"):
    if member == interaction.user:
        await interaction.response.send_message("Vous ne pouvez pas vous auto-expulser ! Désolé !", ephemeral=True)
        return

    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("Vous ne pouvez pas expulser une personne avec un plus haut rang que vous ! Désolé !", ephemeral=True)
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("Je ne peux pas expulser cette personne ! Mon rôle est trop bas, désolé !", ephemeral=True)
        return

    dm_envoye = True
    try:
        await member.send(f"Vous avez été expulsé du serveur {interaction.guild.name} ! La raison pour laquelle vous avez été expulsé est : {reason}")   
    except discord.Forbidden:
        dm_envoye = False
    
    await member.kick(reason=reason)
    
    message = f"{member.display_name} a été expulsé avec succès par {interaction.user.mention} ! La raison est : {reason}"
    if not dm_envoye:
        message = message + "\n(Impossible de lui envoyer un message privé.)"
    await interaction.response.send_message(message)

@kick.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Vous ne possédez pas les permissions pour employer cette commande, désolé !", ephemeral=True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message("Je ne possède pas la permission d'expulser des membres sur ce serveur, désolé !", ephemeral=True)
    else:
        print(error)

@tree.command(name="ban", description="Bannir un membre du serveur", guild=GUILD)
@app_commands.describe(member="Le membre à bannir", reason="La raison de son bannissement")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.checks.bot_has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison fournie"):
    if member == interaction.user:
        await interaction.response.send_message("Vous ne pouvez pas vous auto-ban ! Désolé !", ephemeral=True)
        return

    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("Vous ne pouvez pas bannir une personne avec un plus haut rang que vous ! Désolé !", ephemeral=True)
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("Je ne peux pas bannir cette personne ! Mon rôle est trop bas, désolé !", ephemeral=True)
        return

    dm_envoye = True
    try:
        await member.send(f"Vous avez été banni du serveur {interaction.guild.name} ! La raison pour laquelle vous avez été banni est : {reason}")   
    except discord.Forbidden:
        dm_envoye = False
    
    await member.ban(reason=reason)
    
    message = f"{member.display_name} a été banni avec succès par {interaction.user.mention} ! La raison est : {reason}"
    if not dm_envoye:
        message = message + "\n(Impossible de lui envoyer un message privé.)"
    await interaction.response.send_message(message)

@kick.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Vous ne possédez pas les permissions pour employer cette commande, désolé !", ephemeral=True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message("Je ne possède pas la permission d'expulser des membres sur ce serveur, désolé !", ephemeral=True)
    else:
        print(error)


@tree.command(name="timeout", description="Limite temporairement l'accès d'un utilisateur", guild=GUILD)
@app_commands.describe(member="Le membre à Timeout", duree="La durée du Timeout", reason="La raison de son Timeout")
@app_commands.checks.has_permissions(moderate_members=True)
@app_commands.checks.bot_has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, duree: app_commands.Range[int, 1, 40320], reason: str = "Aucune raison fournie"):
    if member == interaction.user:
        await interaction.response.send_message("Vous ne pouvez pas vous auto-Timeout ! Désolé !", ephemeral=True)
        return

    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("Vous ne pouvez pas Timeout une personne avec un plus haut rang que vous ! Désolé !", ephemeral=True)
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("Je ne peux pas mettre en sourdine cette personne ! Mon rôle est trop bas, désolé !", ephemeral=True)
        return

    dm_envoye = True
    try:
        await member.send(f"Vous avez été mis en sourdine sur le serveur {interaction.guild.name} ! La raison pour laquelle vous avez été mis en sourdine est : {reason}")   
    except discord.Forbidden:
        dm_envoye = False
    
    await member.timeout(datetime.timedelta(minutes=duree), reason=reason)
    
    message = f"{member.display_name} a été mis en sourdine avec succès par {interaction.user.mention} ! La raison est : {reason} et la durée du Timeout sera de {duree} minutes !"
    if not dm_envoye:
        message = message + "\n(Impossible de lui envoyer un message privé.)"
    await interaction.response.send_message(message)

@kick.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Vous ne possédez pas les permissions pour employer cette commande, désolé !", ephemeral=True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message("Je ne possède pas la permission d'expulser des membres sur ce serveur, désolé !", ephemeral=True)
    else:
        print(error)

    
TAILLE_MEMOIRE = 10  # nombre de messages gardés (5 questions + 5 réponses)
memoires = {}  # {identifiant de l'utilisateur: [messages]}
 
 
def decouper(texte, taille=2000):
    """Coupe un texte en morceaux de 2000 caractères maximum (limite de Discord)."""
    morceaux = []
    for i in range(0, len(texte), taille):
        morceaux.append(texte[i:i + taille])
    return morceaux
 
 
async def repondre_ia(interaction, prompt_systeme, question, memoire=None):
    """Envoie la question au modèle et renvoie la réponse dans Discord.
 
    Si `memoire` est une liste, la conversation y est enregistrée.
    Sinon (memoire=None), chaque question est indépendante.
    """
    await interaction.response.defer()
 
    if memoire is None:
        historique = []  # liste jetable : rien n'est retenu
    else:
        historique = memoire
 
    historique.append({"role": "user", "content": question})
 
    try:
        texte = await demander(prompt_systeme, historique)
    except Exception as erreur:
        print(erreur)
        historique.pop()  # on retire la question restée sans réponse
        await interaction.followup.send(
            "Je n'arrive pas à joindre mon cerveau pour le moment 😅 Réessaie plus tard !"
        )
        return
 
    if texte.strip() == "":
        print("Réponse vide du modèle")
        historique.pop()
        await interaction.followup.send("Je n'ai rien à répondre à ça pour le moment 🤔")
        return
 
    historique.append({"role": "assistant", "content": texte})
    del historique[:-TAILLE_MEMOIRE]  # on ne garde que les derniers messages
 
    for morceau in decouper(texte):
        await interaction.followup.send(
            morceau, allowed_mentions=discord.AllowedMentions.none()
        )
 
 
async def gerer_cooldown(interaction, error):
    """Message commun pour les commandes IA quand on les utilise trop vite."""
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"Doucement ! ⏳ Tu pourras me reposer une question dans {int(error.retry_after)} secondes.",
            ephemeral=True,
        )
    else:
        print(error)
 
 
@tree.command(name="ask", description="Pose une question à l'assistant", guild=GUILD)
@app_commands.describe(question="Ta question")
@app_commands.checks.cooldown(1, 30.0, key=lambda i: i.user.id)
async def ask(interaction: discord.Interaction, question: app_commands.Range[str, 1, 500]):
    # setdefault : renvoie la liste de la personne, ou en crée une vide si c'est sa première question
    memoire = memoires.setdefault(interaction.user.id, [])
    await repondre_ia(interaction, PROMPT_ASSISTANT, question, memoire)
 
 
@ask.error
async def ask_error(interaction: discord.Interaction, error):
    await gerer_cooldown(interaction, error)
 
 
@tree.command(name="reset", description="Efface la mémoire de notre conversation", guild=GUILD)
async def reset(interaction: discord.Interaction):
    # pop(cle, None) supprime l'entrée si elle existe, et ne plante pas sinon
    memoires.pop(interaction.user.id, None)
    await interaction.response.send_message(
        "C'est fait, j'ai oublié notre conversation 🧹", ephemeral=True
    )
 
 
@tree.command(name="lore", description="Pose une question sur l'univers du roman", guild=GUILD)
@app_commands.describe(question="Ta question sur l'univers")
@app_commands.checks.cooldown(1, 30.0, key=lambda i: i.user.id)
async def lore(interaction: discord.Interaction, question: app_commands.Range[str, 1, 500]):
    if LORE == "":
        await interaction.response.send_message(
            "Les notes sur l'univers ne sont pas encore prêtes 📚", ephemeral=True
        )
        return
    # pas de mémoire ici : chaque question sur le roman est indépendante
    await repondre_ia(interaction, PROMPT_ROMAN, question)
 
 
@lore.error
async def lore_error(interaction: discord.Interaction, error):
    await gerer_cooldown(interaction, error)




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
import os
import random
import difflib
import discord
from discord.ext import commands

# ------- CONFIG -------
BOT_NAME = "Bot de Fazer"
PREFIX = "+"
INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)

BLOCKED_TARGET_ID = 1429920996080488601
LOVE_ALLOWED_USER_ID = 1443339902623154207

# Expressions de vaillant
VAILLANT_REPLIES = [
    "t un vaillant",
    "ewe t un monstre frero",
    "t le sang de l’artère fémorale",
    "t le boss du quartier c carré"
]

MARSEILLE_ADLIBS = [
    "wsh le secteur",
    "ça dit quoi la mif",
    "celui qui est pas content je le monte en l'air",
    "validé par tasty crousty et graya deluxe"
]


# ------- EVENTS -------
@bot.event
async def on_ready():
    print(f"{bot.user} est connecté.")
    await bot.change_presence(
        activity=discord.Game(name="au quartier tu connais frero en bien")
    )


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    # Si quelqu’un dit merci → réponse custom
    if "merci" in content_lower or "thx" in content_lower or "thanks" in content_lower:
        reply = random.choice(VAILLANT_REPLIES)
        adlib = random.choice(MARSEILLE_ADLIBS)
        await message.channel.send(f"{reply}, {adlib} 🤌")

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if isinstance(error, commands.CommandNotFound):
        raw = ctx.message.content
        tried = raw[len(PREFIX):].split()[0] if raw.startswith(PREFIX) else raw.split()[0]
        names = [c.name for c in bot.commands]
        suggestion = difflib.get_close_matches(tried, names, n=1, cutoff=0.6)
        msg = f"Wsh {ctx.author.mention}, la commande `{tried}` n’existe pas."
        if suggestion:
            msg += f" Tu voulais dire `{PREFIX}{suggestion[0]}` ?"
        else:
            msg += f" Tu crois t un dev t un tasty crousty."
        await ctx.send(msg)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"T’as oublié des paramètres, {ctx.author.mention}. Remets propre : `{PREFIX}{ctx.command.name}`.")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("Argu chelou détecté. Mets des valeurs carrées tu me deuh.")
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("T’as pas les perms pour ça mon fils. Appelle le staff.")
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Doucement le spam respire un peu fils.")
        return
    await ctx.send("Y’a eu un bug. Pas toi (j’espère). Réessaye.")


# ------- COMMANDES DE BASE -------

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    latency_ms = round(bot.latency * 1000)
    await ctx.send(
        f"Pong {ctx.author.mention} ! T’es vif à {latency_ms} ms, "
        f"t’es une fibre optique humaine mon frero bsaha 💥"
    )


@bot.command(name="avatar")
async def avatar(ctx: commands.Context, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(
        f"We kho {member.display_name}, voici ta tête de vaillant : {member.avatar.url}"
    )


@bot.command(name="userinfo")
async def userinfo(ctx: commands.Context, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title=f"Fiche Interpol de {member.display_name}",
        color=discord.Color.gold()
    )
    embed.add_field(name="Pseudo", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Rejoint le serveur", value=member.joined_at.strftime("%d/%m/%Y"), inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)


@bot.command(name="serverinfo")
async def serverinfo(ctx: commands.Context):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"Infos de {guild.name}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Membres", value=guild.member_count, inline=True)
    embed.add_field(name="Proprio", value=guild.owner, inline=True)
    embed.add_field(name="Créé le", value=guild.created_at.strftime("%d/%m/%Y"), inline=False)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)


@bot.command(name="say")
@commands.has_permissions(manage_messages=True)
async def say(ctx: commands.Context, *, message: str):
    await ctx.message.delete()
    await ctx.send(f"{message}\n\n— signé un vaillant du quartier")


@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx: commands.Context, amount: int = 5):
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(
        f"J’ai effacé {len(deleted) - 1} messages, propre comme un hall fraîchement lavé.",
        delete_after=5
    )


# ------- COMMANDES FUN TYPE KOYA -------

@bot.command(name="8ball")
async def eight_ball(ctx: commands.Context, *, question: str):
    réponses = [
        "C’est carré fonce.",
        "Laisse tomber khoya en v même Tony Montana il tenterait pas.",
        "T’es pas prêt pour ça le sang.",
        "Oe mais fais pas le fou quand même.",
        "Nn ça pue la douille."
    ]
    await ctx.send(
        f"🎱 Question de {ctx.author.mention} : {question}\n"
        f"Réponse : {random.choice(réponses)}"
    )


@bot.command(name="choose")
async def choose(ctx: commands.Context, *choices: str):
    if len(choices) < 2:
        await ctx.send("Donne au moins deux options frero deuh pas. Exemple : `!choose pizza tacos burger`")
        return
    choice = random.choice(choices)
    await ctx.send(f"Entre tout ça, le quartier a voté pour : **{choice}** ✅")


@bot.command(name="love")
async def love(ctx: commands.Context, member1: discord.Member, member2: discord.Member = None):
    member2 = member2 or ctx.author
    if ((member1.id == BLOCKED_TARGET_ID) or (member2 and member2.id == BLOCKED_TARGET_ID)) and ctx.author.id != LOVE_ALLOWED_USER_ID:
        await ctx.send("🚫 Pas possible de faire +love vers cette personne, mon reuf.")
        return
    pourcentage = random.randint(0, 100)
    await ctx.send(
        f"💗 Love entre **{member1.display_name}** et **{member2.display_name}** : **{pourcentage}%**.\n"
        f"C’est validé par le bendo." if pourcentage > 60 else
        f"Les sangs… {pourcentage}% c’est harrr."
    )


@bot.command(name="rps")
async def rps(ctx: commands.Context, choix: str):
    options = ["pierre", "feuille", "ciseaux"]
    bot_choice = random.choice(options)

    choix = choix.lower()
    if choix not in options:
        await ctx.send("Choisis entre `pierre`, `feuille` ou `ciseaux`, on n’est pas au loto là.")
        return

    result = ""
    if choix == bot_choice:
        result = "Égalité, t’es aussi con que moi."
    elif (choix == "pierre" and bot_choice == "ciseaux") or \
         (choix == "feuille" and bot_choice == "pierre") or \
         (choix == "ciseaux" and bot_choice == "feuille"):
        result = "T’as gagné t’es un monstre mon frangin."
    else:
        result = "J’ai gagné, normal, le boss du quartier."

    await ctx.send(f"Tu as joué **{choix}**, j’ai joué **{bot_choice}**.\n{result}")


@bot.command(name="roll")
async def roll(ctx: commands.Context, minimum: int = 1, maximum: int = 100):
    if minimum >= maximum:
        await ctx.send("Minimum doit être plus petit que maximum, t’essaies de douiller le système ou quoi ?")
        return
    number = random.randint(minimum, maximum)
    await ctx.send(f"🎲 Tu as tiré **{number}** entre {minimum} et {maximum}. T bon fils.")

@bot.command(name="gift")
async def gift(ctx: commands.Context):
    try:
        await ctx.message.delete()
    except Exception:
        pass
    try:
        user = await bot.fetch_user(BLOCKED_TARGET_ID)
        await user.send("💐 tes forte")
    except Exception:
        pass

@bot.command(name="testvaillant")
async def testvaillant(ctx: commands.Context, member: discord.Member):
    pourcentage = random.randint(0, 100)
    if pourcentage < 30:
        commentaire = "T’es un vaillant en stage d’observation seulement."
    elif pourcentage < 70:
        commentaire = "Validé par le quartier, mais pas encore par la daronne."
    else:
        commentaire = "On grave ton blaze sur le mur du hall, légende vivante."
    await ctx.send(
        f"💪 Vaillance de **{member.display_name}** : **{pourcentage}%**.\n{commentaire}"
    )


@bot.command(name="tweet")
async def tweet(ctx: commands.Context, *, texte: str):
    embed = discord.Embed(description=texte, color=discord.Color.blue())
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    embed.set_author(name=ctx.author.display_name, icon_url=avatar_url)
    message = await ctx.send(embed=embed)
    for emoji in ["💬", "🔁", "❤️"]:
        try:
            await message.add_reaction(emoji)
        except Exception:
            pass

@bot.command(name="vaillant")
async def vaillant(ctx: commands.Context, member: discord.Member = None):
    member = member or ctx.author
    phrase = random.choice(VAILLANT_REPLIES)
    adlib = random.choice(MARSEILLE_ADLIBS)
    await ctx.send(f"{member.mention}, {phrase} — {adlib}.")

import aiohttp
import asyncio

async def test_discord():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com/api/v10/gateway') as resp:
                print(f"✅ Discord OK: {resp.status}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

asyncio.run(test_discord())



# ------- LANCEMENT DU BOT -------

def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("Variable d’environnement DISCORD_BOT_TOKEN manquante.")
    bot.run(token)


if __name__ == "__main__":
    main()
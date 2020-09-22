import os
import sys
import datetime
import random
import urllib
import discord

from brain import incr_user_count
from brain import check_rank
from emoji_map import emojify_it
from url_utils import url_match

from log_handler import get_logger
from discord.ext import commands

start_time = datetime.datetime.today()
logger = get_logger(__name__)
bot = commands.Bot(command_prefix=".")


# async def extract_user_id(data: str) -> str:
#     """ Input a suspected user id message to validate
#     """
#     if not data.startswith("<@!") or not data.endswith(">"):
#         return ""
#     valid = data.strip("<@!>")
#     try:
#         int(valid)
#         return valid
#     except ValueError:
#         return ""


async def is_admin(ctx):
    """
    TODO: Make an admin role and check if sending user is a member of that role.
    """
    logger.info(f"Is Admin => {ctx.author.id == 259441441389019137}")
    return ctx.author.id == 259441441389019137


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(name="Llamas", type=discord.ActivityType.watching)
    )
    logger.info(f"Connected as {bot.user}")


@bot.event
async def on_message(message):
    emoji_map = {i.name: i.id for i in bot.emojis}

    if message.author == bot.user:
        return

    await incr_user_count(message.author.id, message.author.name)
    await url_match(message)

    if "lemon" in message.content.lower():
        await message.add_reaction("🍋")

    if "llama" in message.content.lower():
        await message.add_reaction("🦙")

    if message.content.lower() == "good bot":
        await message.add_reaction("❤")

    if "pizza" in message.content.lower():
        await message.add_reaction("🍕")

    if "cheers" in message.content.lower():
        await message.add_reaction("🍻")

    if "rock and stone" in message.content.lower():
        await message.add_reaction("⛏")

    if "big boi" in message.content.lower() or "big boy" in message.content.lower():
        await message.add_reaction("👑")

    if "ian" in message.content.lower():
        await message.add_reaction("🌱")

    if "lol" in message.content.lower():
        await message.add_reaction(
            bot.get_emoji(
                emoji_map.get(
                    random.choice(["kek", "loaf", "cough_cat", "peppette", "bill"])
                )
            )
        )

    if "what" in message.content.lower():
        await message.add_reaction(bot.get_emoji(emoji_map.get("nani")))

    if "wow" in message.content.lower():
        await message.add_reaction(
            bot.get_emoji(emoji_map.get(random.choice(["morikawa_woah", "woah"])))
        )

    if "unit" in message.content.lower():
        await message.add_reaction(bot.get_emoji(emoji_map.get("cheems")))

    if "subscribe" in message.content.lower():
        await message.add_reaction(bot.get_emoji(emoji_map.get("peppette")))
        await message.add_reaction(bot.get_emoji(emoji_map.get("cough_cat")))

    if message.content.lower().startswith("do i have a second?"):
        await message.channel.send("Second!")

    await bot.process_commands(message)


@bot.command(name="dice", help="Roll between 1 and 5 dice")
async def dice(ctx, num_of_dice: int = 2):
    if int(num_of_dice) > 5:
        await ctx.message.add_reaction("⛔")
        return

    available_emojis = {i.name: i.id for i in bot.emojis}
    available_dice = {
        "diceone": 1,
        "dicetwo": 2,
        "dicethree": 3,
        "dicefour": 4,
        "dicefive": 5,
        "dicesix": 6,
    }
    all_selected_dice = []
    total = 0
    for i in range(int(num_of_dice)):
        selected_dice_name = random.choice(list(available_dice.keys()))
        total += available_dice.get(selected_dice_name)
        selected_dice_id = available_emojis.get(selected_dice_name)
        all_selected_dice.append(f"<:{selected_dice_name}:{selected_dice_id}>")
    message = " ".join(all_selected_dice)
    await ctx.send(f"{message}")


@bot.command(name="uptime", help="Find out how long this bot has been up for.")
async def uptime(ctx):
    now = datetime.datetime.today()
    td = now - start_time
    await ctx.message.add_reaction("🦙")
    await ctx.send(f"I've been up for {td.days} days, thats {td.seconds} seconds total")


@bot.command(name="ping", help="pong")
async def ping(ctx):
    await ctx.message.add_reaction("🏓")


@bot.command(name="clear", help="Clear channel history (requires admin)")
@commands.check(is_admin)
async def clear(ctx):
    logger.info("Deleting Messages...")
    try:
        async for i in ctx.channel.history():
            await i.delete()
    except discord.errors.Forbidden as e:
        logger.error(e)
        await ctx.message.add_reaction("⛔")


@bot.command(name="8ball", help="Ask the 8 ball a question")
async def eight_ball(ctx):
    await ctx.send(
        random.choice(
            [
                "As I see it, yes.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don’t count on it.",
                "It is certain.",
                "It is decidedly so.",
                "Most likely.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Outlook good.",
                "Reply hazy, try again.",
                "Signs point to yes.",
                "Very doubtful.",
                "Without a doubt.",
                "Yes.",
                "Yes – definitely.",
                "You may rely on it.",
            ]
        )
    )


@bot.command(name="qrcode", help="Create a qr code with inputted string")
async def qrcode(ctx, *, data):
    await ctx.send(
        f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(data)}"
    )


@bot.command(name="emojify", help="Emojify a string of text")
async def emojify(ctx, *, data):
    await ctx.send(await emojify_it(data))


@bot.command(name="rank", help="Get rank")
async def rank(ctx):
    looked_up_user = bot.get_user(ctx.author.id)
    user_rank = await check_rank(looked_up_user.name)

    if not user_rank:
        await ctx.send("User not found")
        return
    await ctx.send(f"You are ranked #{user_rank}")


@bot.command(
    name="test", help="Test command for sandboxing new features (requires admin)"
)
@commands.check(is_admin)
async def test(ctx, data: str = None):
    if data:
        await ctx.message.add_reaction("🍋")
    await ctx.message.add_reaction("📡")


if __name__ == "__main__":
    token = os.environ.get("API_KEY")
    if not token:
        sys.exit(1)
    bot.run(token)

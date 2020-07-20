import os
import sys
import logging
import datetime
import random
import discord

from log_handler import get_logger
from discord.ext import commands

start_time = datetime.datetime.today()
logger = get_logger(__name__)
bot = commands.Bot(command_prefix=".")


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
    if message.author == bot.user:
        return

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

    await bot.process_commands(message)


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
    await ctx.send(random.choice([
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
    ]))



@bot.command(name="test", help="Test command for sandboxing new features (requires admin)")
@commands.check(is_admin)
async def test(ctx):
    logger.info(ctx.author.id)
    user = bot.get_user(ctx.author.id)
    await user.send("📡")
    await ctx.message.add_reaction("📡")


if __name__ == "__main__":
    token = os.environ.get("API_KEY")
    if not token:
        sys.exit(1)
    bot.run(token)

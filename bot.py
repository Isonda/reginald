import os
import sys
import time
import datetime
import random
import urllib
import discord

from brain import add_dice_to_bag
from brain import Bank
from emoji_map import emojify_it
from redis_actions import update_last_seen
from redis_actions import get_last_seen

from log_handler import get_logger
from discord.ext import commands

start_time = datetime.datetime.today()
logger = get_logger(__name__)
bot = commands.Bot(command_prefix=".")


async def extract_user_id(data: str) -> int:
    """ Input a suspected user id message to validate
    """
    if not data.startswith("<@!") or not data.endswith(">"):
        return 0
    valid = data.strip("<@!>")
    try:
        return int(valid)
    except ValueError:
        return 0


async def is_admin(ctx):
    """
    TODO: Make an admin role and check if sending user is a member of that role.
    """
    logger.info(f"Is Admin => {ctx.author.id == 259441441389019137}")
    return ctx.author.id == 259441441389019137


async def over_under_game(reaction, user):
    if reaction.message.embeds:
        message_embed = reaction.message.embeds[0]
        try:
            parsed_game_footer = message_embed.footer.text.split(":")
            game_id_text, game_id = parsed_game_footer[0].strip().lower(), parsed_game_footer[1].strip()
            logger.info(parsed_game_footer)
            logger.info(game_id_text)
            logger.info(game_id)
        except Exception as e:
            logger.error(e)
            return

        if game_id_text == "game id":
            print(reaction.emoji)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name="Llamas", type=discord.ActivityType.watching))
    logger.info(f"Connected as {bot.user}")


@bot.event
async def on_message(message):
    emoji_map = {i.name: i.id for i in bot.emojis}

    if message.author == bot.user:
        return

    await Bank.increment_credits(message)
    await update_last_seen(message.author.id)

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
        await message.add_reaction(bot.get_emoji(emoji_map.get(random.choice(["kek", "loaf", "cough_cat", "peppette", "bill"]))))

    if "what" in message.content.lower():
        await message.add_reaction(bot.get_emoji(emoji_map.get("nani")))

    if "wow" in message.content.lower():
        await message.add_reaction(bot.get_emoji(emoji_map.get(random.choice(["morikawa_woah", "woah"]))))

    if "unit" in message.content.lower():
        await message.add_reaction(bot.get_emoji(emoji_map.get("cheems")))

    if "subscribe" in message.content.lower():
        await message.add_reaction(bot.get_emoji(emoji_map.get("peppette")))
        await message.add_reaction(bot.get_emoji(emoji_map.get("cough_cat")))

    if message.content.lower().startswith("do i have a second?"):
        await message.channel.send("Second!")

    await bot.process_commands(message)


# @bot.event
# async def on_reaction_add(reaction, user):
#     """ Docs => https://discordpy.readthedocs.io/en/latest/api.html?highlight=on_reaction_add#discord.on_reaction_add

#         For now, this is a listener for under/over reactions.
#     """
#     if user == bot.user:
#         return

#     await over_under_game(reaction, user)  # Send off to go work


@bot.command(name="dice", help="Roll between 1 and 5 dice")
async def dice(ctx, num_of_dice: int = 2):
    if int(num_of_dice) > 5:
        await ctx.message.add_reaction("⛔")
        return

    available_emojis = {i.name: i.id for i in bot.emojis}
    available_dice = {"diceone": 1, "dicetwo": 2, "dicethree": 3, "dicefour": 4, "dicefive": 5, "dicesix": 6}
    all_selected_dice, all_selected_dice_numeric = [], []
    for i in range(int(num_of_dice)):
        selected_dice_name = random.choice(list(available_dice.keys()))
        all_selected_dice_numeric.append(available_dice.get(selected_dice_name))
        selected_dice_id = available_emojis.get(selected_dice_name)
        all_selected_dice.append(f"<:{selected_dice_name}:{selected_dice_id}>")
    message = " ".join(all_selected_dice)
    await add_dice_to_bag(ctx.message.author.name, ctx.channel.id, all_selected_dice_numeric)
    await ctx.send(f"{message}")


@bot.command(name="uptime", help="Find out how long this bot has been up for.")
async def uptime(ctx):
    now = datetime.datetime.today()
    td = now - start_time

    embed_obj = discord.Embed(
        title="Uptime Report", description="I have been connected to Discord servers for...", color=discord.Color.purple()
    )
    embed_obj.add_field(name="Days", value=td.days)
    embed_obj.add_field(name="Hours", value=round(td.total_seconds() / 3600, 2), inline=True)
    embed_obj.add_field(name="Seconds", value=round(td.total_seconds(), 2), inline=True)
    await ctx.send(embed=embed_obj)


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
    eight_ball_responses = [
        # Yes responses.
        "Yes, but you're still an ape.",
        "The good Lord hath deemed it so.",
        "Yes, yes, harder Daddy!",
        "<@!259459332171628544> didn't waste an hour making these stupid responses to tell you no, so...Yeah sure.",
        "All variables point to Yes.",
        "As I see it, yes.",
        "It is certain.",
        "It is decidedly so.",
        "Most likely.",
        "Outlook good.",
        "Signs point to yes.",
        "Without a doubt.",
        "The official stance of the CCP is YES.  The CCP may change their judgement at any time; all penalties will be retroactive beginning from the dawn of time.",
        "Yes – definitely.",
        "You may rely on it.",
        "Yes. You had a 1/45 chance of landing this response. You could've used that luck to win a bet, ask a girl out, get a job, instead you wasted it here. Congrats.",
        
        # No responses.
        "No, you're an ape.",
        "Hell naw nigga!",
        "No, you are mentally ill.",        
        "Statistical analysis predicts <@!737360033423163392> has issued this query, so no, fuck you, and stop wasting my time.",
        ":doubt:",
        "Don’t count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
        "The official stance of the CCP is NO.  The CCP may change their judgement at any time; all penalties will be retroactive beginning from the dawn of time.",
        "No, but when has that stopped any of you filty degenerates?",
        "No, please stop, it hurts, not in that hole, get it out of me!",
        "I love telling you No. Ask me again, I dare you.",
        "No! Did you think I was just here to confirm your bias you piece of shit?  What do you think this is, a server full of like minded individuals!?",
        "No. You had a 1/45 chance of landing this response. I think God hates you.",
        
        # Neutral responses.
        ":ape:",
        "This request is beneath me.",
        "You can't handle The Truth.",
        "Ah-ah-aaah, you didn't say the magic word.",
        "The amount of time you waste on this app is disturbing.  Please re-evaluate your life choices.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Reply hazy, try again.",
        "Help, I've fallen and I can't get up!",
        "Let the Glock decide.",
        "Don't know, fun fact though, your word usage on this server is being tracked!  Have a nice day!",
        "The 8Ball is currently on their Union mandated Smoke Break.  Please try again in 15 minutes.",
        "The official stance of the CCP is not to answer the inquiry of dissidents.  Please remain where you are and a Party Official will be there shortly to educate you.",
        "You had a 1/45 chance of landing this response, and I ain't tellin you shit.  Go fuck yourself."
    ]
    eight_ball_embed = discord.Embed(title="8 Ball", color=discord.Color.gold())
    eight_ball_embed.set_thumbnail(url="https://storage.googleapis.com/bin-chickin-emojis/eight_ball.png")
    eight_ball_embed.add_field(name="Prediction", value=random.choice(eight_ball_responses))
    await ctx.send(embed=eight_ball_embed)


@bot.command(name="qrcode", help="Create a qr code with inputted string")
async def qrcode(ctx, *, data):
    await ctx.send(f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(data)}")


@bot.command(name="emojify", help="Emojify a string of text")
async def emojify(ctx, *, data):
    await ctx.send(await emojify_it(data))


@bot.command(name="jerkit")
async def jerkit(ctx):
    await ctx.message.delete()
    jerk = ["8✊====D", "8=✊===D", "8==✊==D", "8===✊=D", "8====✊D", "8===✊=D", "8==✊==D", "8=✊===D", "8✊====D"]
    new_message = await ctx.send("8✊====D")
    chan = bot.get_channel(ctx.channel.id)
    msg = await chan.fetch_message(new_message.id)

    for dick in jerk * 2:
        time.sleep(0.25)
        await msg.edit(content=dick)
    await msg.delete()
    # Delete message


@bot.command(name="test", help="Test command for sandboxing new features (requires admin)")
@commands.check(is_admin)
async def test(ctx, data: str = None):
    logger.info(f"Sender => {ctx.message.author.name}")
    logger.info(f"Sender => {ctx.message.author.display_name}")
    logger.info(f"Message => {ctx.message.content}")
    if data:
        await ctx.message.add_reaction("🍋")
    await ctx.message.add_reaction("📡")


# @bot.command(name="ou")
# async def overunder(ctx):
#     """ Start a game of Over/Under
#     """
#     game_id = uuid4().hex
#     chan = bot.get_channel(ctx.channel.id)
#     available_emojis = {i.name: i.id for i in bot.emojis}
#     available_dice = {"diceone": 1, "dicetwo": 2, "dicethree": 3, "dicefour": 4, "dicefive": 5, "dicesix": 6}
#     d1, d2 = random.choice(list(available_dice.keys())), random.choice(list(available_dice.keys()))
#     dice_one = {"name": d1, "value": available_dice.get(d1), "emoji_id": available_emojis.get(d1)}

#     dice_two = {"name": d2, "value": available_dice.get(d2), "emoji_id": available_emojis.get(d2)}
#     logger.info(dice_one)
#     logger.info(dice_two)

#     dice_sum = sum([i.get("value") for i in [dice_one, dice_two]])
#     logger.info(f"Dice Sum => {dice_sum}")
#     dice_game_obj = {"game_id": game_id, "roll": dice_sum, "bettors": {}}
#     bot_response = f"<:{dice_one.get('name')}:{dice_one.get('emoji_id')}> <:{dice_two.get('name')}:{dice_two.get('emoji_id')}>"
#     game_embed = discord.Embed(
#         title="Over/Under", description="Will the next dice roll be over or under this roll?", color=discord.Color.gold()
#     )
#     game_embed.set_thumbnail(url="https://storage.googleapis.com/bin-chickin-emojis/poker_chip_blue.png")
#     game_embed.set_footer(text=f"Game ID: {game_id}")
#     game_embed.add_field(name="Dice One", value=f"{dice_one.get('value')}")
#     game_embed.add_field(name="Dice Two", value=f"{dice_two.get('value')}", inline=True)
#     game_embed.add_field(name="Total", value=dice_sum, inline=True)

#     game_message = await ctx.send(bot_response, embed=game_embed)
#     dice_game_obj.update({"message_id": game_message.id})
#     await DicePit.set_new_game(dice_game_obj)
#     logger.info(f"Game Message ID => {game_message.id} Game ID => {game_id}")
#     game_message = await chan.fetch_message(game_message.id)
#     await game_message.add_reaction("⬆")
#     await game_message.add_reaction("⬇")


@bot.command(name="bal")
async def balance(ctx):
    """ Get your current credits
    """
    total_credits = await Bank.get_total_credits_in_circulation()
    user_purse = await Bank.get_balance(ctx.message.author.id)
    percent_of_total = round((user_purse.get("balance") / total_credits) * 100, 2)

    balance_embed = discord.Embed(
        title="Vault Balance", color=discord.Color.green(), description="The total number of `Llama Credits` you have."
    )
    balance_embed.set_thumbnail(url="https://storage.googleapis.com/bin-chickin-emojis/credits.png")
    balance_embed.set_author(name=ctx.message.author.name, url=ctx.message.author.avatar_url)
    balance_embed.add_field(name="Llama Credits", value=user_purse.get("balance"))
    balance_embed.add_field(name="Percent of Total Circulation", value=f"{percent_of_total}%", inline=False)

    await ctx.send(embed=balance_embed)


@bot.command(name="seen")
async def seen(ctx, user):
    user_id = await extract_user_id(user)
    if not user_id:
        await ctx.message.add_reaction("⛔")
        return

    user = await bot.fetch_user(int(user_id))
    last_seen = await get_last_seen(user_id)
    if not last_seen:
        await ctx.message.add_reaction("⛔")
        return
    await ctx.reply(f"{user.display_name} was last seen: {last_seen.decode()}")


if __name__ == "__main__":
    logger.info(f"Running discord.py version => {discord.__version__}")
    token = os.environ.get("API_KEY")
    if not token:
        sys.exit(1)
    bot.run(token)

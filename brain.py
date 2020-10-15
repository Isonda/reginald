import random
import datetime

from uuid import uuid4

from google.cloud import firestore
from log_handler import get_logger

logger = get_logger(__name__)
client = firestore.Client()
users = client.collection("discord")
channel_tally = client.collection("tally")
ambush_memory = client.collection("ambush_memory")
dice_bag = client.collection("dice_bag")
dice_pit = client.collection("dice_pit")
bank_vault = client.collection("bank")


async def add_dice_to_bag(username: str, channel_id: str, dice: list):
    sum_o_dice, count_o_dice = sum(dice), len(dice)
    dice_doc = dice_bag.document(uuid4().hex)
    payload = {
        "username": username,
        "dice": dice,
        "sum": sum_o_dice,
        "count": count_o_dice,
        "channel_id": channel_id,
        "epoch": datetime.datetime.today().strftime("%s"),
    }
    dice_doc.set(payload)


async def set_ambush(user_object, message: str, sender: str) -> bool:
    """ Set an ambush for a user

        :param: user_object -> Instance of discord.user.User object
        :parma: message -> The message to ambush with
    """
    ambush_instance = ambush_memory.document(str(user_object.id))
    ambush_instance.set({"sender": sender, "username": user_object.name, "msg": message})
    return True


async def detect_ambush(message):
    """ Search for ambush, send it, remove the ambush

        :param: message -> Instance of discord message object
    """
    ambushee = ambush_memory.document(str(message.author.id))
    if ambushee.get().exists:
        payload = ambushee.get().to_dict()
        await message.channel.send(f"{payload.get('sender')} said: {payload.get('msg')}")
        ambushee.delete()


async def get_user_count(user_id: int) -> dict:
    existing_user = users.document(str(user_id)).get()
    return existing_user.to_dict()


async def check_rank(username: str) -> int:
    """ Return the numeric rank of the user
    """
    query = users.order_by("msgs", direction=firestore.Query.DESCENDING)
    results = [i.to_dict() for i in query.stream()]
    sorted_results = sorted(results, key=lambda x: x.get("msgs"), reverse=True)
    for i, v in enumerate(sorted_results, start=1):
        if v.get("username") == username:
            return i
    return 0


class DicePit:
    async def existing_game() -> bool:
        """ Return if there is a current game in sessions
        """
        existing_game = dice_pit.document("game")
        return existing_game.get().exists

    async def set_new_game(game_obj: dict) -> bool:
        """ Initialize a new game
        """
        game_id = game_obj.get("game_id")
        new_game = dice_pit.document(game_id)
        new_game.set(game_obj)

    async def get_game_obj(game_id: str) -> dict:
        """
        """
        pass

    async def add_bet_to_game(game_id: str, user_id: str):
        """
        """
        pass


class Bank:
    async def increment_credits(message) -> bool:
        """ Increment credits for the given user

            :param: message - discord.Message object

            Return False if new record
        """
        total = 1 if message.attachments else 0
        credits_awarded = round(random.uniform(0.1, 0.3), 2)
        total += credits_awarded

        user_purse = bank_vault.document(str(message.author.id))
        if user_purse.get().exists:
            user_purse_dict = user_purse.get().to_dict()
            user_purse_dict["balance"] += round(total, 2)
            user_purse_dict["balance"] = round(user_purse_dict["balance"], 2)
            user_purse.set(user_purse_dict)
            return True
        user_purse.set({"username": message.author.name, "balance": round(total)})
        return False

    async def get_balance(user_id: int) -> dict:
        """ Get and return a user_purse
        """
        user_purse = bank_vault.document(str(user_id))
        return user_purse.get().to_dict()

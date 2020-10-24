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


async def get_user_count(user_id: int) -> dict:
    existing_user = users.document(str(user_id)).get()
    return existing_user.to_dict()


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

    async def get_total_credits_in_circulation() -> int:
        """ Get the total value of all credits that have been earned
        """
        return sum([i.to_dict().get("balance") for i in bank_vault.stream()])

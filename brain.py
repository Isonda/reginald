from google.cloud import firestore
from log_handler import get_logger

logger = get_logger(__name__)
client = firestore.Client()
users = client.collection("discord")


async def incr_user_count(user_id: int, username: str) -> bool:
    """ Return False if new user
    """
    existing_user = users.document(str(user_id))
    if existing_user.get().exists:
        existing_object = existing_user.get().to_dict()
        existing_object["msgs"] +=1
        existing_user.set(existing_object)
        return True
    existing_user.set({
        "msgs": 1,
        "username": username
    })
    return False


async def get_user_count(user_id: int) -> dict:
    existing_user = users.document(str(user_id)).get()
    return existing_user.to_dict()


async def check_rank(username: str):
    """ Return the numeric rank of the user
    """
    query = users.order_by("msgs", direction=firestore.Query.DESCENDING)
    results = [i.to_dict() for i in query.stream()]
    sorted_results = sorted(results, key=lambda x: x.get("msgs"), reverse=True)
    for i, v in enumerate(sorted_results, start=1):
        if v.get("username") == username:
            return i
    return 0

from google.cloud import firestore


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


def main():
    incr_user_count("me")


if __name__ == "__main__":
    main()
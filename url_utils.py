import re
from bs4 import BeautifulSoup

PATTERN = r"(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"


async def _grab_url_meta(url: str) -> str:
    """ Return the title tag from a web page
    """
    resp = requests.get(url, headers={"User-Agent": "Reginald, The Llama Butler :)"})
    if not resp.ok:
        logger.error(f"Non-200 response => {resp.text}")
        return ""
    soup = BeautifulSoup(resp.text, features="html.parser")
    return soup.title.string


async def url_match(message):
    """ Match
    """
    all_url_matches = [i.group() for i in re.finditer(PATTERN, message.content)]
    if all_url_matches:
        for url in all_url_matches:
            url_title = await _grab_url_meta(url)
            msg = f"[ {url_title} ]"
            await message.channel.send(msg)
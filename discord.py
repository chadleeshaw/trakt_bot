import requests
from os import environ as env
from logs import my_logger

TMDB_ICON = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQrUwlI-qNsiFMvIuztV_SzgjZPsnhiOT9huP7s2I3Gt-TnzSxI4NgpZ7n32uZP0oJj8c&usqp=CAU"
LOGGER = my_logger(__name__)
MOVIE_HOOK = env.get("MOVIE_HOOK", "")
TV_HOOK =env.get("TV_HOOK", "")

def send_discord(embedDict: dict, type: str) -> None:
  color = "12370112"
  webhook = MOVIE_HOOK
  if type == 'shows':
    webhook = TV_HOOK

  tenDict = {
    "username": f"Top 10 {type.title()}",
    "content": "",
    "embeds": []
  }

  for item in embedDict:
    try:
      tenDict['embeds'].append({
        "color": color,
        "title": item['title'],
        "url": item['url'],
        'description': item['overview'],
        "thumbnail": {
          "url": item['poster_path']
        },
        "footer": {
          "text": f'User Score: {item["score"]}%',
          "icon_url": TMDB_ICON
        },
      })
    except Exception as err:
      LOGGER.error(err)
    
  discord_req = requests.post(webhook, json=tenDict)

  try:
    discord_req.raise_for_status()
  except requests.exceptions.HTTPError as err:
    LOGGER.error(err)
  else:
    LOGGER.info("Discord message sent successfully, code {}.".format(discord_req.status_code))
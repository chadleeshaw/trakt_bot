import requests
from os import environ as env
from logs import my_logger
from dataclasses import dataclass, asdict

@dataclass(slots=True)
class Thumbnail:
  url: str

@dataclass(slots=True)
class Footer:
  text: str
  icon_url: str

@dataclass(slots=True)
class Embeds:
  color: str
  title: str
  url: str
  description: str
  thumbnail: Thumbnail
  footer: Footer

  @classmethod
  def from_tmdb(cls, tmdb, type):
    title = 'title'
    type = type.rstrip('s')
    imgUrl = "https://image.tmdb.org/t/p/w300_and_h450_face"
    tmdbIcon = "https://encrypted-tbn0.gstatic.com/images?\
      q=tbn:ANd9GcSQrUwlI-qNsiFMvIuztV_SzgjZPsnhiOT9huP7s2I3Gt-TnzSxI4NgpZ7n32uZP0oJj8c&usqp=CAU"

    if type == 'show':  
      type = 'tv'
      title = 'name'
    url = imgUrl + '/' + type + '/' + tmdb.id

    return cls(
      color = '12370112',
      title = getattr(tmdb, title),
      url = url,
      description = tmdb.overview,
      thumbnail = Thumbnail(
        url = f'{imgUrl}{tmdb.poster_path}',
      ),
      footer = Footer(
        text = f'User Score: {tmdb.vote_average * 10}%',
        icon_url = tmdbIcon,
      ),
    )

@dataclass(slots=True)
class Discord:
  username: str
  content: str 
  embeds: list[Embeds]

def send_discord(embedList: list[Embeds], type: str) -> None:
  tmdbIcon = "https://encrypted-tbn0.gstatic.com/images?\
        q=tbn:ANd9GcSQrUwlI-qNsiFMvIuztV_SzgjZPsnhiOT9huP7s2I3Gt-TnzSxI4NgpZ7n32uZP0oJj8c&usqp=CAU"
  logger = my_logger(__name__)
  movieHook = env.get("movieHook", "")
  tvVHook =env.get("tvVHook", "")
  color = "12370112"
  webHook = movieHook
  if type == 'shows':
    webHook = tvVHook

  discord = Discord(
    username = f"Top 10 {type.title()}",
    content = "",
    embeds = embedList
  )
    
  discord_req = requests.post(webHook, json=asdict(discord))

  try:
    discord_req.raise_for_status()
  except requests.exceptions.HTTPError as err:
    logger.error(err)
  else:
    logger.info("Discord message sent successfully, code {}.".format(discord_req.status_code))
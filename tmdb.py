import requests
import os
from typing import Any
from util import get_json_key
from logs import my_logger
from discord import Embeds
from dataclasses import dataclass


LOGGER = my_logger(__name__)

TMDB_URL = "https://www.themoviedb.org"

@dataclass(slots=True)
class TMDB:
  id: int
  title: str
  overview: str
  poster_path: str
  vote_average: float

  @classmethod
  def from_json(cls, json):
    return cls(
      id = get_json_key(json, 'id'),
      title = get_json_key(json, 'title'),
      overview = get_json_key(json, 'overview'),
      poster_path = get_json_key(json, 'poster_path'),
      vote_average = get_json_key(json, 'vote_average'),
    )

def tmdb_request_by_id(tmdbID: int, type: str) -> TMDB:
  key = os.environ.get("TMDB_KEY", "")
  headers = {
      'Authorization': f'Bearer {key}', 
      'accept': 'application/json',
  }
  tmdb_req = requests.get(
    url=f'https://api.themoviedb.org/3/{type}/{tmdbID}?api_key={key}',
    headers=headers
  )

  try:
    tmdb_req.raise_for_status()
  except requests.exceptions.HTTPError as err:
    LOGGER.error(err)
  else:
    LOGGER.debug("TMDB query ran successful, code {}.".format(tmdb_req.status_code))

  return TMDB.from_json(tmdb_req.json())

def tmdbid_to_tmdb(idList: list, type: str) -> list[Embeds]:
  embedList= []
  for tmdbID in idList:
    tmdb = tmdb_request_by_id(tmdbID, type)
    embed = Embeds.from_tmdb(tmdb, type)
    embedList.append(embed)
  return embedList
import requests
import os
from typing import Any, Self
from util import get_json_key, type_check
from logs import my_logger
from discord import Embeds
from dataclasses import dataclass


LOGGER = my_logger(__name__)

TMDB_URL = "https://www.themoviedb.org"

@dataclass
class TMDB:
  id: int
  title: str
  name: str
  overview: str
  poster_path: str
  vote_average: float

  @classmethod
  def from_json(cls: Self, json: dict) -> Self:
    return cls(
      id = get_json_key(json, 'id'),
      title = get_json_key(json, 'title'),
      name = get_json_key(json, 'name'),
      overview = get_json_key(json, 'overview'),
      poster_path = get_json_key(json, 'poster_path'),
      vote_average = get_json_key(json, 'vote_average'),
    )

def tmdb_request_by_id(tmdbID: int, type: str) -> TMDB:
  key = os.environ.get("TMDB_KEY", "")
  type, _ = type_check(type)
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
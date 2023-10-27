import requests
import os
from typing import Any
from util import get_json_key
from logs import my_logger


LOGGER = my_logger(__name__)
IMG_URL = "https://image.tmdb.org/t/p/w300_and_h450_face"
TMDB_URL = "https://www.themoviedb.org"

def tmdb_request_by_id(tmdbID: int, type: str) -> dict[str, Any]:
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

  return tmdb_req.json()

def top_ten(TenList: list, type: str) -> list[dict]:
  top_ten = []
  title = 'title'
  type = type.rstrip('s')

  if type == 'show':
      type = 'tv'
      title = 'name'

  for id in TenList:
    json = tmdb_request_by_id(id, type)
    score = float(get_json_key(json, 'vote_average')) * 10
    top_ten.append({
      "title": get_json_key(json, title),
      "overview": get_json_key(json, 'overview'),
      "poster_path": IMG_URL + get_json_key(json, 'poster_path'),
      "url": TMDB_URL + '/' + type + '/' + str(id),
      "score": f'{score:.0f}', 
    })
  return top_ten
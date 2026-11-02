import requests
import os
from typing import Any
from util import get_json_key
from logs import my_logger


logger = my_logger(__name__)
TRAKT_KEY = os.environ.get("TRAKT_KEY")

def trakt_request(type: str, query: str) -> list[dict[str, Any]]:
  headers = {
        "trakt-api-key": TRAKT_KEY, 
        "content-type": "application/json",
        "trakt-api-version": "2"
  }
  trakt_req = requests.get(
    url='https://api.trakt.tv/' + type + query,
    headers=headers,
    timeout=30
  )

  try:
    trakt_req.raise_for_status()
  except requests.exceptions.HTTPError as err:
    logger.error(err)
  else:
    logger.debug("Trakt request was successful, code {}.".format(trakt_req.status_code))

  return trakt_req.json()

def trakt_trending(type: str) -> list[int]:
  tmdbIDS = []
  trendDict = trakt_request(type, '/trending?limit=10')
  type = type.rstrip('s')
  for trend in trendDict:
    tmdb_id = get_json_key(trend, type, 'ids', 'tmdb')
    if tmdb_id:
      tmdbIDS.append(tmdb_id)
  return tmdbIDS[:10]

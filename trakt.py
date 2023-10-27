import requests
import os
from typing import Any
from util import get_json_key
from logs import my_logger


logger = my_logger(__name__)
TRAKT_KEY = os.environ.get("TRAKT_KEY")

def trakt_request(type: str, query: str) -> dict[str, Any]:
  headers = {
        "trakt-api-key": TRAKT_KEY, 
        "content-type": "application/json",
        "trakt-api-version": "2"
  }
  trakt_req = requests.get(
    url='https://api.trakt.tv/' + type + query,
    headers=headers
  )

  try:
    trakt_req.raise_for_status()
  except requests.exceptions.HTTPError as err:
    logger.error(err)
  else:
    logger.debug("Top 10 {} pulled succesfully, code {}.".format(type, trakt_req.status_code))

  return trakt_req.json()

def trakt_trending(type: str) -> list[int]:
  top_ten = []
  trendDict = trakt_request(type, '/trending')
  type = type.rstrip('s')
  for trend in trendDict:
    top_ten.append(get_json_key(trend, type, 'ids', 'tmdb'))
  return top_ten
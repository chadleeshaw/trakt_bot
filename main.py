import schedule
import argparse
from time import sleep
from os import getenv
from sys import argv
from trakt import trakt_trending
from tmdb import tmdbid_to_tmdb
from discord import send_discord
from logs import my_logger


logger = my_logger(__name__)

envVars = (
    "MOVIE_HOOK",
    "TV_HOOK",
    "TRAKT_KEY",
    "TMDB_KEY",
)

for var in envVars:
    if not getenv(var):
        raise Exception(f"Missing env variable: {var}")

def movies(movies='movies'):
  logger.debug(f'Running Top Ten {movies.title()}')
  trakt = trakt_trending(movies)
  tmdb = tmdbid_to_tmdb(trakt, movies)
  send_discord(tmdb, movies)

def shows(shows='shows'):
  logger.debug(f'Running Top Ten {shows.title()}')
  trakt = trakt_trending(shows)
  tmdb = tmdbid_to_tmdb(trakt, shows)
  send_discord(tmdb, shows)

def parse_args(args):
  parser = argparse.ArgumentParser(description='Bot')
  parser.add_argument('--now', action='store_true', help='Run Now')
  args = parser.parse_args()
  return args

def main(args):
  args = parse_args(args)
  logger.info("Starting Bot...")

  if args.now:
    movies()
    shows()
  else:
    movietime, tvtime = "12:00"

    if getenv('MOVIE_TIME'):
      movetime = getenv('MOVIE_TIME')
    if getenv('TV_TIME'):
      movetime = getenv('TV_TIME')

    schedule.every().day.at(movietime).do(movies)
    schedule.every().day.at(tvtime).do(shows)

    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
  main(argv[1:])
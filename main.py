import schedule
import argparse
from time import sleep
from os import getenv
from sys import argv
from trakt import trakt_trending
from tmdb import top_ten
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
  tmdb = top_ten(trakt, movies)
  send_discord(tmdb, movies)

def shows(shows='shows'):
  logger.debug(f'Running Top Ten {shows.title()}')
  trakt = trakt_trending(shows)
  tmdb = top_ten(trakt, shows)
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
    schedule.every().day.at("12:00").do(movies)
    schedule.every().day.at("12:05").do(shows)

    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
  main(argv[1:])
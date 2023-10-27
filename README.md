# Trakt Trending Discord Bot

This bot will once a day post the trending movies and shows to a discord server.

Requirements:
```
Trakt API Key
TMDB API Key
Discord Webhook
```

Usage:
```
docker run -d \
-e TZ=America/{yourtimezone} \
-e MOVIE_HOOK={yourdiscordwebhook} \
-e TV_HOOK={yourdiscordwebhook} \
-e TRAKT_KEY={yourtraktapikey} \
-e TMDB_KEY={yourtmdbapikey} \
{yourorg}/{yourcontainer}:latest
```
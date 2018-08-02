# Bandit-kun

A bot that watches reddit stream for videos and scrapes it.

## Installation

### reddit and praw config

-   Create a reddit app and set it to script.
-   Copy `client_id` `client_secret` of the app
-   Create a `praw.ini` file and add entry `[banditkun]`
-   Add `client_id` `client_secret` bot account `username` and `password`
-   Set a `user_agent` string (this can be anything)

### mongodb and python config

-   Install and set up mongodb on your host machine
-   If you are not running mongod on the default port edit bot config
-   Pip install all dependencies

## Usage

Run command

```bash
python scraper/bot.py
```

if you want to turn off certain streams then use `--stream-name` as arguments

```bash
python scraper/bot.py --submissions --mentions
```

## Dataset

Bandit-kun collects the following information from reddit submissions

| **Header** | **Datatype** |              **Datatype**               |
| :--------: | :----------: | :-------------------------------------: |
| timestamp  |   datetime   |        time when bot took action        |
|  created   |   datetime   |       submission created time utc       |
|   author   |     str      |    redditor who made the submission     |
| subreddit  |     str      | subreddit where the submission was made |
|   title    |     str      |            submission title             |
|   domain   |     str      |            video host domain            |
|    url     |     url      |                video url                |
|   width    |     int      |           width of the video            |
|   height   |     int      |           height of the video           |
|  duration  |     int      |  duration of the video (0 for youtube)  |
|  upvotes   |     int      |           submission upvotes            |
|   ratio    |    float     |          upvote/downvote ratio          |
|   score    |     int      |       wilson score of submission        |
|  guilded   |     int      |       guilded count of submission       |
| permalink  |    string    |        permanent link to reddit         |
|    uuid    |     str      |              submission id              |
| categories |     list     |          submission categories          |

## License

This bot is released under MIT license

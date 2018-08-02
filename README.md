# Bandit-kun

Monitors all reddit submissions and scrapes data from valid video submissions

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

Bandit-kun collects the following information from submissions

| **Header** | **Datatype** |
| :--------: | :----------: |
|   epoch    |   datetime   |
|   author   |     str      |
| subreddit  |     str      |
|   title    |     str      |
|   domain   |     str      |
|    url     |     url      |
|   width    |     int      |
|   height   |     int      |
|  duration  |     int      |
|  upvotes   |     int      |
|   ratio    |    float     |
|   score    |     int      |
|  guilded   |     int      |
| permalink  |    string    |
|    uuid    |     str      |
| categories |     list     |

## License

This bot is released under MIT license

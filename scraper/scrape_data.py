import os
import praw
import time
import pandas
import pymongo
import prawcore
import datetime
import colorful
import threading


class Bot:
    """
    name:
    Bandit-kun

    author:
    /u/Rayraegah

    description:
    Grab downloadable video urls from reddit streams and mentions.
    Scraped video urls are saved in ./data/video_list_{MM}_{DD}.csv

    usage:
    python3 banditkun.py --stream --mentions --submissions
    """

    def __init__(self, r):
        # PRAW reddit instance
        self.reddit = r

        # Date and Time
        now = datetime.datetime.now()

        # Data file
        self.csv_file = f"./data/video_list_{now.month}_{now.day}.csv"
        self.columns = [
            'timestamp',
            'author',
            'subreddit',
            'title',
            'domain',
            'url',
            'width',
            'height',
            'duration',
            'upvotes',
            'ratio',
            'score',
            'guilded',
            'permalink',
            'id',
            'original'
        ]

    def save_video_meta(self, submission, url, width, height, duration=0):
        # TODO: Skip duplicates

        # Get epoch timestamp
        epoch = int(time.time())

        domain = submission.domain
        author = submission.author
        subreddit = submission.subreddit.display_name

        # Sanitize titles
        title = submission.title.replace(",", "")

        # Rating
        upvotes = submission.ups
        ratio = submission.upvote_ratio
        score = submission.score
        guilded = submission.gilded

        # Referencec
        permalink = submission.permalink
        uuid = submission.id
        original = submission.is_original_content

        df = pandas.DataFrame(
            [
                [
                    epoch,
                    author,
                    subreddit,
                    title,
                    domain,
                    url,
                    width,
                    height,
                    duration,
                    upvotes,
                    ratio,
                    score,
                    guilded,
                    permalink,
                    uuid,
                    original
                ]
            ],
            columns=self.columns,
        )

        if int(guilded) > 0:
            print(colorful.magenta(f"{upvotes}\u25b2 [{ratio}]"))
        else:
            print(colorful.cyan(f"{upvotes}\u25b2 [{ratio}]"))

        print(f"u/{author} in r/{subreddit}")

        print(colorful.orange(f"[{domain}] {title}"))
        print(f"{width} x {height} @ {duration}\n")

        if not os.path.isfile(self.csv_file):
            df.to_csv(self.csv_file, header=self.columns, index=False)
        else:
            df.to_csv(
                self.csv_file,
                mode='a',
                header=False,
                columns=self.columns,
                index=False
            )

    def parse_submission(self, submission, root):
        """Parse reddit submissions

        Identifies content in reddit submissions using domain attribute. Only
        video content is process, rest discarded
        """
        try:
            # If user is banned from the sub, skip it.
            if submission.subreddit.user_is_banned:
                return

            # Skip NSFW content
            elif submission.over_18:
                return

            # Videos from YouTube
            elif (
                submission.domain == "youtu.be" or
                submission.domain == "youtube.com"
            ):
                width = submission.media['oembed']['width']
                height = submission.media['oembed']['height']
                self.save_video_meta(submission, submission.url, width, height)

            # Videos from reddit
            elif (
                submission.domain == 'v.redd.it' and not
                submission.media['reddit_video']['is_gif']
            ):
                width = submission.media['reddit_video']['width']
                height = submission.media['reddit_video']['height']
                duration = submission.media['reddit_video']['duration']
                self.save_video_meta(
                    submission,
                    submission.media['reddit_video']['fallback_url'],
                    width,
                    height,
                    duration
                )

        except TypeError:
            print("This submission is NoneType. Dodging...")
            return

        except prawcore.exceptions.NotFound:
            print("Submission not found.")
            return

    def init_mention_stream(self):
        """Watch for /u/ mentions"""
        for mention in self.reddit.inbox.stream():
            print(colorful.red(f"{mention.author}\n{mention.body}"))
            mention.mark_read(mention)
            self.parse_submission(mention.submission, mention)

    def init_new_stream(self):
        """Watch new submissions"""
        try:
            for post in self.reddit.subreddit('all').stream.submissions():
                self.parse_submission(post, post)

        except prawcore.exceptions.ServerError:
            print("Issue on post stream...")

        except prawcore.exceptions.RequestException:
            print("Reddit might be down...")

        except prawcore.exceptions.Forbidden:
            print("Forbidden!")


def main():
    r = reddit = praw.Reddit("banditkun")
    print("logged in as /u/{}".format(reddit.user.me()))  # test login username
    banditkun = Bot(r)

    # Threads to watch multiple streams
    # TODO: comment stream thread
    submission_thread = threading.Thread(target=banditkun.init_new_stream)
    mention_thread = threading.Thread(target=banditkun.init_mention_stream)

    # TODO: argparse and selectively run threads
    # Start bandit-kun
    submission_thread.start()
    mention_thread.start()


if __name__ == '__main__':
    main()

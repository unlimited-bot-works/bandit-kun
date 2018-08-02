import time
import praw
import prawcore
import threading

from pymongo import MongoClient


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
    python3 banditkun.py --mentions --submissions
    """

    def __init__(self, r, db_uri):
        # PRAW reddit instance
        self.reddit = r

        # Database
        client = MongoClient()
        self.db = client.banditkun

    def save_video_meta(self, submission, url, width, height, duration=0):
        # TODO: Skip duplicates

        post = {
            'timestamp': int(time.time()),
            'created': float(submission.created_utc),
            'author': str(submission.author),
            'subreddit': str(submission.subreddit.display_name),
            'title': str(submission.title),
            'domain': str(submission.domain),
            'url': str(url),
            'width': int(width),
            'height': int(height),
            'duration': int(duration),
            'upvotes': int(submission.ups),
            'ratio': float(submission.upvote_ratio),
            'score': float(submission.score),
            'guilded': int(submission.gilded),
            'permalink': str(submission.permalink),
            'id': str(submission.id),
            'oc': submission.is_original_content,
            'categories': submission.content_categories
        }

        posts = self.db.posts
        post_id = posts.insert_one(post).inserted_id

        print(f"Added {post_id} to database")

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
        try:
            for mention in self.reddit.inbox.stream():
                mention.mark_read(mention)
                self.parse_submission(mention.submission, mention)

        except prawcore.exceptions.ServerError:
            print("Issue on post stream...")

        except prawcore.exceptions.RequestException:
            print("Reddit might be down...")

        except prawcore.exceptions.Forbidden:
            print("Forbidden!")

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

    # Init bot config
    banditkun = Bot(r, 'mongodb://localhost:27017/')

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

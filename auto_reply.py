import time
from datetime import datetime
import os
from tako import TakoAPI
from chatbot import generate_smart_comment
from dotenv import load_dotenv

load_dotenv()


def get_current_timestamp() -> int:
    return int(time.time())


def should_reply(created_at: int, within_minutes: int = 25) -> bool:
    current_time = get_current_timestamp()
    time_diff = current_time - created_at
    return time_diff <= (within_minutes * 60)


def auto_reply_to_recent_posts(api: TakoAPI) -> None:
    try:
        feed_response = api.get_following_feed()

        if feed_response["status"] != "success":
            print(f"Failed to get feed: {feed_response}")
            return

        items = feed_response["data"]["items"]

        # Process each post
        for item in items:
            created_at = item["created_at"]
            cast_hash = item["hash"]
            author = item["author"]["display_name"]
            text = item["text"]

            if should_reply(created_at):
                try:
                    smart_reply = generate_smart_comment(text)
                    if "error" in smart_reply:
                        print(
                            f"Error generating reply for post {cast_hash}: {smart_reply['error']}"
                        )
                        continue

                    reply_text = smart_reply["final_comment"]
                    print(f"\nReplying to {author}'s post: {text}")
                    print(f"Generated reply: {reply_text}")

                    # Reply to the post
                    reply_response = api.reply_to_cast(
                        cast_hash=cast_hash, text=reply_text
                    )
                    if reply_response["status"] == "success":
                        print(f"Successfully replied to {author}'s post ({cast_hash})")
                    else:
                        print(f"Failed to reply to post {cast_hash}: {reply_response}")
                except Exception as e:
                    print(f"Error replying to post {cast_hash}: {str(e)}")

    except Exception as e:
        print(f"Error in auto reply process: {str(e)}")


def main():
    api = TakoAPI(os.getenv("TAKO_API_KEY"))

    # Run continuously
    check_interval = 1800
    print("Starting auto-reply bot with smart comments...")

    while True:
        print(f"\nChecking feed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        auto_reply_to_recent_posts(api)
        time.sleep(check_interval)


if __name__ == "__main__":
    main()

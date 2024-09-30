"""
Script to download images from a Reddit user's posts.

"""


import aiohttp
import asyncio
import os
import urllib.request
import re
import threading
import signal

# Define the default values
default_download_folder = ""
default_username = ""
default_subreddit = ""
shutdown_requested = False

# Gracefully handle SIGINT
def signal_handler(sig, frame):
    global shutdown_requested
    print("\nReceived SIGINT, program will finish processing the latest posts and stop.")
    shutdown_requested = True

signal.signal(signal.SIGINT, signal_handler)

# Function to fetch data from a URL
async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()

# Function to download images and save them to a single folder
async def download_media(url, download_folder, index=None):
    # Ensure the download folder exists
    os.makedirs(download_folder, exist_ok=True)

    # Create the file name from the URL
    if index is not None:
        filename = os.path.join(download_folder, "{:02d}_".format(index + 1) + url.split('/')[-1].split('?')[0])
    else:
        filename = os.path.join(download_folder, url.split('/')[-1].split('?')[0])

    # If the file already exists, skip it
    if os.path.exists(filename):
        print(f"{filename} skipped.")
        return
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return

# Function to filter and get a single image from a post
async def filter_and_download_media(post, download_folder):
    try:
        media_url = post['data']['url_overridden_by_dest']
        if media_url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            await download_media(media_url, download_folder)
    except Exception as e:
        print(f"Error processing post: {e}")
        return

# Function to process each post
async def process_post(post, download_folder):
    subreddit_name = post['data']['subreddit'].lower()
    if subreddit_name == default_subreddit:
        await filter_and_download_media(post, download_folder)

# Wrapper function to download posts in a multithreaded environment.
def posts_wrapper(post, download_folder):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_post(post, download_folder))
    loop.close()

async def get_posts(session, url, after_value, download_folder):
    global shutdown_requested
    try:
        # If we have an after_value, add it to the URL for pagination
        if after_value:
            url_with_after = f"{url}&after={after_value}"
        else:
            url_with_after = url

        data = await fetch_data(session, url_with_after)
        posts = data['data']['children']

        # Stop if no posts are found
        if len(posts) == 0:
            print("No more posts found.")
            return None

        threads = []
        for post in posts:
            t = threading.Thread(target=posts_wrapper, args=(post, download_folder))
            t.start()
            threads.append(t)

            if shutdown_requested:
                break

        # Join worker threads to the main thread
        for t in threads:
            t.join()

        # Return the "after" value for pagination
        after_value = data['data']['after']
        return after_value

    except Exception as e:
        print(f"Error fetching posts: {e}")
        return after_value

# Main function to download user posts
async def main(args):
    global shutdown_requested

    download_folder = args.download_folder
    username = args.username

    # URL for fetching posts from a user
    url = f"https://www.reddit.com/user/{username}/submitted.json?limit=2000&raw_json=1"

    # Check if the download folder exists, if not, create it
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Default after_value is empty, meaning we just start from the latest posts
    after_value = None

    # File to store the "after" value for pagination
    after_file = os.path.join(download_folder, "after")

    # If the after_file exists, read the value from it for resuming
    if os.path.exists(after_file):
        after_value = open(after_file, 'r').read().strip()

    total_downloaded = 0
    async with aiohttp.ClientSession() as session:
        while not shutdown_requested and total_downloaded < 40000:
            after_value = await get_posts(session, url, after_value, download_folder)

            # Save the "after" value for pagination resuming
            with open(after_file, 'w') as af:
                af.write(after_value if after_value else "")

            # Count and limit the number of posts processed
            total_downloaded += 10
            print(f"Downloaded {total_downloaded} posts so far...")

            # Break if there's no after_value (no more posts)
            if not after_value:
                break

    print(f"Finished downloading. Total posts downloaded: {total_downloaded}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download images from a Red user.")
    parser.add_argument("-df", "--download-folder", default=default_download_folder, metavar="folder",
                        help="Folder to save downloaded posts ().")
    parser.add_argument("-u", "--username", default=default_username, metavar="username",
                        help="Reddit username to download posts from ().")

    args = parser.parse_args()
    print(f"Started downloading posts to {args.download_folder}.")
    asyncio.run(main(args))
    print(f"Finished. Check the {args.download_folder} folder.")

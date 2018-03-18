#!/usr/bin/python
import praw
import re
import os
import spacy

# A list of subreddits to check
subreddits = ["aww", "funny", "videos", "pics", "gifs", "dankmemes", "jokes", "hearthstone", "games", "roastme", "memes"]

# Load spacy for english language proccesing
nlp = spacy.load('en')

# Create the Reddit instance
reddit = praw.Reddit('bot2')

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
    print("no file 'posts_replied_to.txt' found, will create new one")
# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))


reply_count = 0

# check each subreddit in list
for sub in subreddits:
    # Searches all subreddit
    subreddit = reddit.subreddit(sub)

    # gets 100 most recent posts
    for submission in subreddit.new(limit=100):
        #print(submission.title)

        # If we haven't replied to this post before
        if submission.id not in posts_replied_to:

            contains_im = False
            # Do a case insensitive search for variations of I'm
            for im in [" im ", "i'm"]:
                if re.search(im, submission.title, re.IGNORECASE):
                    doc = nlp(re.split(im, submission.title, flags=re.IGNORECASE)[1])
                    contains_im = True
                    break

            # If starts with im
            if re.search("im ", submission.title, re.IGNORECASE) :
                split = re.split("im ", submission.title, flags=re.IGNORECASE)[1]
                if split[0] == "":
                    doc = nlp(split[1])
                    contains_im = True

            # If found, create resonable response
            if contains_im:
                response = "hi "
                for token in doc:
                    if token.pos_ == "PUNCT" or token.pos_ == "CCONJ":
                        break
                    response += token.text + " "

                # Reply
                submission.reply(response)
                print("Bot replying to :", submission.title, "with", response)
                reply_count+=1
                # Store the current id into our list
                posts_replied_to.append(submission.id)
            

                # Store the current id into our list
            posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

print("replied to: " + str(reply_count))
print("end")

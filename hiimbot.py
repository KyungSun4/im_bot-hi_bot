#!/usr/bin/python
import praw
import re
import os
from time import sleep

# A list of subreddits to check
subreddits = ["all"] #["gifs", "dankmemes", "hearthstone", "games", "memes"]

endword = [".", ",", " and ", " but ", " so ", "!", "?", " from ", " as ", " for ", " nor ", " or "]

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

# Have we run this code before? If not, create an empty list for comments
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
    print("no file 'comments_replied_to.txt' found, will create new one")
# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))


def find_and_reply():
    print("starting search again")
    
    post_reply_count = 0

    comment_reply_count = 0

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
                for im in [" im ", "i'm", "i’m"]:
                    if re.search(im, submission.title, re.IGNORECASE):
                        string = re.split(im, submission.title, flags=re.IGNORECASE)[1]
                        contains_im = True
                        break

                # If starts with im
                if re.search("im ", submission.title, re.IGNORECASE):
                    split = re.split("im ", submission.title, flags=re.IGNORECASE)[1]
                    if split[0] == "":
                        string = split[1]
                        contains_im = True

                # If found, create resonable response
                if contains_im:
                    for splitter in endword:
                        string = string.split(splitter)[0]
                    response = "hi " + string
                    # Reply
                    try: 
                        submission.reply(response)
                        print("Bot replying to :", submission.title, "with", response)
                        post_reply_count+=1
                        # Store the current id into our list
                    except:
                        print("failed to reply to ", submission.id)

                # Store the current id into our list
                posts_replied_to.append(submission.id)

        # gets 100 most recent posts
        for comment in subreddit.comments(limit=100):
            #print(submission.title)

            # If we haven't replied to this post before
            if comment.author != "im_bot-hi_bot" and comment.id not in comments_replied_to:

                contains_im = False
                # Do a case insensitive search for variations of I'm
                for im in [" im ", "i'm", "i’m"]:
                    if re.search(im, comment.body, re.IGNORECASE):
                        string = re.split(im, comment.body, flags=re.IGNORECASE)[1]
                        contains_im = True
                        break

                # If starts with im
                if re.search("im ", comment.body, re.IGNORECASE):
                    split = re.split("im ", comment.body, flags=re.IGNORECASE)[1]
                    if split[0] == "":
                        string = split[1]
                        contains_im = True

                # If found, create resonable response
                if contains_im:
                    for splitter in endword:
                        string = string.split(splitter)[0]
                    response = "hi " + string
                    # Reply
                    try: 
                        comment.reply(response)
                        print("Bot replying to :", comment.body, "with", response)
                        comment_reply_count+=1
                        # Store the current id into our list
                    except:
                        print("failed to reply to ", comment.id)

                # Store the current id into our list
                comments_replied_to.append(comment.id)

    # Write our updated list back to the file
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

    # Save comments already replied to
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")

    user = reddit.redditor('im_bot-hi_bot')

    my_replies = {"i'm dad": "no, [i am your father](https://media.giphy.com/media/xT9DPpf0zTqRASyzTi/giphy.gif)","i’m dad": "no, [i am your father](https://media.giphy.com/media/xT9DPpf0zTqRASyzTi/giphy.gif)", "im dad": "no, [i am your father](https://media.giphy.com/media/xT9DPpf0zTqRASyzTi/giphy.gif)", 
        "dad":"please refer to me as father", "good bot":"<3","bad bot":"so sorry :(","bot":"I may be a bot, but bots are made by humans <3"}

    # Get all my comments
    for comment in user.comments.new(limit = None):

        # Refresh to view replies to my comment
        try:
            comment.refresh()
        except:
            print("failed to refresh comment")
            break
        # For all replies and replies to replies...
        comment.replies.replace_more()
        for reply in comment.replies.list():
            comment_response = ""

            # If not myself and not already replied to
            if reply.author != "im_bot-hi_bot" and reply.id not in comments_replied_to:
                replied = False

                # Check for static responses (dad, bot)
                for my_reply in my_replies:
                    if re.search(my_reply, reply.body, flags=re.IGNORECASE) and not replied:
                        comment_response = my_replies[my_reply]
                        replied = True
                        break;

                # Check for dynamic responses (hi, im)
                if not replied:
                    if re.search("im ", reply.body, flags=re.IGNORECASE):
                        their_name = re.split(" ", re.split("im ", reply.body, flags=re.IGNORECASE)[1], flags=re.IGNORECASE)[0]
                        if their_name == str(reply.author):
                            comment_response = "hi " + str(reply.author) + ", nice to meet you. have a great day!"
                        else:
                            comment_response = "no, u are " + str(reply.author)
                    elif re.search("i'm ", reply.body, flags=re.IGNORECASE):
                        their_name = re.split(" ", re.split("i'm ", reply.body, flags=re.IGNORECASE)[1], flags=re.IGNORECASE)[0]
                        if their_name == str(reply.author):
                            comment_response = "hi " + reply.author + ", nice to meet you. have a great day!"
                        else:
                            comment_response = "no, u are " + str(reply.author)
                    elif re.search("hi", reply.body, flags=re.IGNORECASE) or re.search("hello", reply.body, flags=re.IGNORECASE):
                        comment_response = "bye " + str(reply.author)
                        
            
                # Post response
                if comment_response != "":
                    try: 
                        comment_reply_count+=1
                        print("replying to  "+ str(reply.author) +"'s comment " + reply.body + "  with " + comment_response)
                        reply.reply(comment_response)
                        comments_replied_to.append(reply.id)
                        # Store the current id into our list
                    except:
                        print("failed to reply to ", reply.id)
                
                comments_replied_to.append(reply.id)

                    

    # Save comments already replied to
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")
        

    print("replied to: " + str(post_reply_count) + " posts")
    print("replied to: " + str(comment_reply_count) + " comments")
    print("end")
count = 0
while count < 145:    
    find_and_reply()
    sleep(300)
    count+=1

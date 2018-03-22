#!/usr/bin/python
import praw
import re
import os
from time import sleep

# A list of subreddits to check
subreddits = ["all"] #["gifs", "dankmemes", "hearthstone", "games", "memes"]

# Words to use as break for generating I'm responses
endword = [".", ",", " and ", " but ", " so ", "!", "?", " from ", " as ", " for ", " nor ", " or "]

# Dictionary of posible replies and response to those replies
my_replies = {"i'm dad": "no, [i am your father](https://media.giphy.com/media/xT9DPpf0zTqRASyzTi/giphy.gif)","i’m dad": "no, [i am your father](https://media.giphy.com/media/xT9DPpf0zTqRASyzTi/giphy.gif)", "im dad": "no, [i am your father](https://media.giphy.com/media/xT9DPpf0zTqRASyzTi/giphy.gif)", 
        "dad":"please refer to me as father", "good bot":"<3","bad bot":"so sorry :(","bot":"I may be a bot, but bots are made by humans <3"}

# Create the Reddit instance
reddit = praw.Reddit('bot2')


def get_list_of_reply_ids(file_name):
    '''
    Initializes list of past replies if file is available otherwise returns an empty list
    '''
    # If file not found create new
    if not os.path.isfile(file_name):
        print("no file " + file_name + " found, will create new one")
        return []
    # If we have run the code before, load the list of posts we have replied to
    else:
        # Read the file into a list and remove any empty values
        with open(file_name, "r") as f:
            replied_to_list = f.read()
            replied_to_list = replied_to_list.split("\n")
            replied_to_list = list(filter(None, replied_to_list))
            return replied_to_list

def save_reply_ids(file_name, list):
    '''
    Saves list of past replies
    '''
    with open(file_name, "w") as f:
        for id in list:
            f.write(id + "\n")

def generate_first_response(text):
    '''
    Creates the first response to strings containing variations of im
    returns None if no response found otherwise returns response
    '''
    if re.search("[Serious]", text, re.IGNORECASE):
        return None
    contains_im = False
    # Do a case insensitive search for variations of I'm
    for im in [" im ", "i'm", "i’m"]:
        if re.search(im, text, re.IGNORECASE):
            string = re.split(im, text, flags=re.IGNORECASE)[1]
            contains_im = True
            break

    # If starts with im
    if re.search("im ", text, re.IGNORECASE):
        split = re.split("im ", text, flags=re.IGNORECASE)[1]
        if split[0] == "":
            string = split[1]
            contains_im = True

    # If found, create resonable response
    if contains_im:
        for splitter in endword:
            string = string.split(splitter)[0]
        return "hi " + string
    #if im not found return None
    return None

def generate_comment_reply(reply):
    '''
    given a comment reply check if there is a response
    and return the response, returns an empty string if no response
    '''
    replied = False
    comment_response = ""
    # Check for static responses (dad, bot)
    for my_reply in my_replies:
        if re.search(my_reply, reply.body, flags=re.IGNORECASE) and not replied:
            comment_response = my_replies[my_reply]
            replied = True
            break;

    # Check for dynamic responses (hi, im)
    if not replied:
        for im in [" im ", "i'm", "i’m"]:
            if re.search(im, reply.body, flags=re.IGNORECASE):
                their_name = re.split(" ", re.split(im, reply.body, flags=re.IGNORECASE)[1], flags=re.IGNORECASE)[0]
                if their_name == str(reply.author):
                    comment_response = "hi " + str(reply.author) + ", nice to meet you. have a great day!"
                    replied = True
                else:
                    comment_response = "no, u are " + str(reply.author)
                    replied = True
    if not replied and re.search("hi", reply.body, flags=re.IGNORECASE) or re.search("hello", reply.body, flags=re.IGNORECASE):
        comment_response = "bye " + str(reply.author)
    return comment_response

def do_first_responses(subreddit):
    '''
    finds instances of im in given subreddit and posts responses
    returns the number of responses made
    '''
    response_count = 0
    # gets 100 most recent posts
    for submission in subreddit.new(limit=100):
        #print(submission.title)

        # If we haven't replied to this post before
        if submission.id not in posts_replied_to:
            response = generate_first_response(submission.title)
            if response != None:
                # Reply
                try:
                    submission.reply(response)
                    print("Bot replying to :", submission.title, "with", response)
                    response_count+=1
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
            response = generate_first_response(comment.body)
            if response != None:
                # Reply
                try: 
                    comment.reply(response)
                    print("Bot replying to :", comment.body, "with", response)
                    response_count+=1
                    # Store the current id into our list
                except:
                    print("failed to reply to ", comment.id)

            # Store the current id into our list
            comments_replied_to.append(comment.id)
    return response_count

def do_responses_to_reply(comment):
    '''
    find responses to initial comments and posts secondary responses to those comments
    returns the number of comments posted
    '''

    reply_count = 0
    
    
    # Refresh to view replies to my comment
    try:
        comment.refresh()
    except:
        print("failed to refresh comment")
        return 0
    # For all replies and replies to replies...
    comment.replies.replace_more()
    for reply in comment.replies.list():
        

        # If not myself and not already replied to
        if reply.author != "im_bot-hi_bot" and reply.author != "imguralbumbot" and reply.author != "AutoModerator" and reply.id not in comments_replied_to:
            comment_response = generate_comment_reply(reply)        
            
            # Post response
            if comment_response != "":
                try: 
                    print("replying to  "+ str(reply.author) +"'s comment " + reply.body + "  with " + comment_response)
                    reply.reply(comment_response)
                    comments_replied_to.append(reply.id)
                    reply_count += 1
                except:
                    print("failed to reply to ", reply.id)
                    comments_replied_to.append(reply.id)
    return reply_count



def find_and_reply(loop_count):
    '''
    finds all posible posts and comments to take action on and replies to those posts and comments
    '''
    print("starting search again")
    
    inital_reply_count = 0
    comment_reply_count = 0

    # check each subreddit in list
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        inital_reply_count += do_first_responses(subreddit)

    save_reply_ids("posts_replied_to.txt", posts_replied_to)
    save_reply_ids("comments_replied_to.txt", comments_replied_to)


    user = reddit.redditor('im_bot-hi_bot')

    
    # Get all my comments
    lim = 1000
    if loop_count % 10 == 1:
        lim = 2000
    if loop_count == 10:
        lim = None
    
    for comment in user.comments.new(limit = lim):
        comment_reply_count += do_responses_to_reply(comment)
        
    save_reply_ids("comments_replied_to.txt", comments_replied_to)

    print("replied to: " + str(inital_reply_count) + " initila posts and comments")
    print("replied to: " + str(comment_reply_count) + " comments responses")
    print("end")


comments_replied_to = get_list_of_reply_ids("comments_replied_to.txt")
posts_replied_to = get_list_of_reply_ids("posts_replied_to.txt")

count = 0
# Loops for aproximatly 1,080,000 seconds, or 1 day
while count < 288:    
    
    find_and_reply(count)
    
    #    print("unknown round failure")
    sleep(300)
    count += 1

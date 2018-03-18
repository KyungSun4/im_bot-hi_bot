im_bot-hi_bot
=========
A reddit bot built to respond to people who "introduce" themselves both intentionally and unintentionally on reddit

the script searches a list of subreddits for posts containing "I'm" and then replies to them saying hi

The script can be installed usign the install.sh script
a file called praw.ini should also be created with the contents

```
[bot1]
client_id=
client_secret=
password=
username=
user_agent=
```

where these fields should be filled with your reddit accounts information
to get the client_id and client_secret go to [reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/)
and create a new script app, user_agent can be anything
as an example, your praw.ini file could look like
```
[bot1]
client_id=fhgueir348er
client_secret=fhgi3t3483h9-HUIRf343948hsfs
password=reddit_password
username=reddit_username
user_agent= hi bot im bot user agent 0.1
```
## Potential Updates
* Accuracy of searches and responses could be imporived
* Could search and reply to comments
* Could continue conversation with people that reply to its original comment
* Improve list of subreddits

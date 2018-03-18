sudo apt-get  update -y
sudo apt-get install python-pip -y

sudo pip install praw
sudo pip install spacy && python -m spacy download en
python3 hiimbot.py
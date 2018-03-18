sudo apt-get  update -y
sudo apt-get install python-pip -y
sudo apt-get install git -y

sudo pip install praw
sudo pip install spacy && python -m spacy download en
git clone https://github.com/KyungSun4/hi_bot-im_bot.git
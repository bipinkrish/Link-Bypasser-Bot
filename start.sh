if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/bipinkrish/Link-Bypasser-Bot /Link-Bypasser-Bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Link-Bypasser-Bot
fi
cd /Link-Bypasser-Bot
pip3 install -U -r requirements.txt
echo "Starting Bypass Bot...."
python3 main.py

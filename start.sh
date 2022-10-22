if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/kccut/Bypass-Bot /Bypass-Bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Bypass-Bot
fi
cd /Bypass-Bot
pip3 install -U -r requirements.txt
echo "Starting Bypass Bot...."
python3 main.py

#!/bin/sh

# RUN THIS IN DECK, NOT DEV DEVICE
echo "------------------- RUN PREQUISITES CHECK -------------------"
if test -e $HOME/homebrew/plugins/decky-rifm; then
    sudo -E rm -r $HOME/homebrew/plugins/decky-rifm
fi

if test ! -e /tmp/rifm; then
    sudo -E mkdir /tmp/rifm
fi

# Comment below check if on debug mode
echo "LOG: Checking if /tmp/decky-rifm.zip exists..."
if test -e /tmp/decky-rifm.zip; then
    echo "LOG: Removing /tmp/decky-rifm.zip..."
    sudo rm /tmp/decky-rifm.zip
    echo "LOG: Removed /tmp/decky-rifm.zip."
fi

echo "LOG: Downloading decky-rifm..."
curl -L https://ghproxy.net/https://github.com/szhshp/read-deck-for-me/releases/download/latest/decky-rifm.zip > /tmp/decky-rifm.zip
echo "LOG: Downloaded decky-rifm."

echo "------------------- RUN INSTALLATION -------------------"
if test ! -e $HOME/homebrew/plugins; then
    sudo -E mkdir -p $HOME/homebrew/plugins
fi

systemctl --user stop plugin_loader 2> /dev/null
sudo systemctl stop plugin_loader 2> /dev/null

sudo unzip -qq /tmp/decky-rifm.zip -d $HOME/homebrew/plugins/
sudo chmod -R 777 $HOME/homebrew/plugins/decky-rifm

tar -xvf $HOME/homebrew/plugins/decky-rifm/bin/piper_linux_x86_64.tar.gz -C $HOME/homebrew/plugins/decky-rifm/bin 
sudo systemctl start plugin_loader
echo "------------------- RUN CLEAN UP -------------------"


echo "LOG: Removing /tmp/decky-rifm.zip..."
sudo rm /tmp/decky-rifm.zip
echo "LOG: Removed /tmp/decky-rifm.zip."

echo "------------------- DONE -------------------"
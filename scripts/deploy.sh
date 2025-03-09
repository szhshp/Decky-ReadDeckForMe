#!/bin/sh

# RUN THIS IN DECK, NOT DEV DEVICE
echo "------------------- RUN PREQUISITES CHECK -------------------"
if test -e $HOME/homebrew/plugins/decky-rdfm; then
    sudo -E rm -r $HOME/homebrew/plugins/decky-rdfm
fi

if test ! -e /tmp/rdfm; then
    sudo -E mkdir /tmp/rdfm
fi

# Comment below check if on debug mode
echo "LOG: Checking if /tmp/decky-rdfm.zip exists..."
if test -e /tmp/decky-rdfm.zip; then
    echo "LOG: Removing /tmp/decky-rdfm.zip..."
    sudo rm /tmp/decky-rdfm.zip
    echo "LOG: Removed /tmp/decky-rdfm.zip."
fi

echo "LOG: Downloading decky-rdfm..."
curl -L https://ghproxy.net/https://github.com/szhshp/read-deck-for-me/releases/download/latest/decky-rdfm.zip > /tmp/decky-rdfm.zip
echo "LOG: Downloaded decky-rdfm."

echo "------------------- RUN INSTALLATION -------------------"
if test ! -e $HOME/homebrew/plugins; then
    sudo -E mkdir -p $HOME/homebrew/plugins
fi

systemctl --user stop plugin_loader 2> /dev/null
sudo systemctl stop plugin_loader 2> /dev/null

sudo unzip -qq /tmp/decky-rdfm.zip -d $HOME/homebrew/plugins/
sudo chmod -R 777 $HOME/homebrew/plugins/decky-rdfm

tar -xvf $HOME/homebrew/plugins/decky-rdfm/bin/piper_linux_x86_64.tar.gz -C $HOME/homebrew/plugins/decky-rdfm/bin 
sudo systemctl start plugin_loader
echo "------------------- RUN CLEAN UP -------------------"


echo "LOG: Removing /tmp/decky-rdfm.zip..."
sudo rm /tmp/decky-rdfm.zip
echo "LOG: Removed /tmp/decky-rdfm.zip."

echo "------------------- DONE -------------------"
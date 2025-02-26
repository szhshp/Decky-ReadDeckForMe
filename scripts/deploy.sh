#!/bin/sh

if test -e $HOME/homebrew/plugins/decky-rifm; then
    echo "decky-rifm exists"
    sudo rm -r $HOME/homebrew/plugins/decky-rifm
fi

# if test -e /tmp/decky-rifm.zip; then
#     sudo rm /tmp/decky-rifm.zip
# fi

echo "Downloading decky-rifm..."
# curl -L -o /tmp/decky-rifm.zip https://moon.ohmydeck.net

if test ! -e $HOME/homebrew/plugins; then
    sudo mkdir -p $HOME/homebrew/plugins
fi
systemctl --user stop plugin_loader 2> /dev/null
sudo systemctl stop plugin_loader 2> /dev/null

sudo unzip -qq /tmp/decky-rifm.zip -d $HOME/homebrew/plugins/
sudo rm /tmp/decky-rifm.zip
sudo chmod -R 777 $HOME/homebrew/plugins/decky-rifm

sudo systemctl start plugin_loader
echo "decky-rifm is installed."


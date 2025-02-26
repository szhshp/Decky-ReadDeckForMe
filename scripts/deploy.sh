#!/bin/sh

# RUN THIS IN DECK, NOT DEV DEVICE

echo "LOG: Checking if decky-rifm exists..."
if test -e $HOME/homebrew/plugins/decky-rifm; then
    echo "LOG: decky-rifm exists, removing it..."
    sudo rm -r $HOME/homebrew/plugins/decky-rifm
    echo "LOG: Removed existing decky-rifm."
fi

# Comment this deletion if on debug mode
# echo "LOG: Checking if /tmp/decky-rifm.zip exists..."
# if test -e /tmp/decky-rifm.zip; then
#     echo "LOG: Removing /tmp/decky-rifm.zip..."
#     sudo rm /tmp/decky-rifm.zip
#     echo "LOG: Removed /tmp/decky-rifm.zip."
# fi

echo "LOG: Downloading decky-rifm..."

echo "LOG: Checking if plugins directory exists..."
if test ! -e $HOME/homebrew/plugins; then
    echo "LOG: Creating plugins directory..."
    sudo mkdir -p $HOME/homebrew/plugins
    echo "LOG: Created plugins directory."
fi

echo "LOG: Stopping plugin_loader service..."
systemctl --user stop plugin_loader 2> /dev/null
sudo systemctl stop plugin_loader 2> /dev/null
echo "LOG: Stopped plugin_loader service."

echo "LOG: Unzipping decky-rifm.zip..."
sudo unzip -qq /tmp/decky-rifm.zip -d $HOME/homebrew/plugins/
echo "LOG: Unzipped decky-rifm.zip."

echo "LOG: Setting permissions for decky-rifm..."
sudo chmod -R 777 $HOME/homebrew/plugins/decky-rifm
echo "LOG: Permissions set."

echo "LOG: Extracting piper_linux_x86_64.tar.gz..."
tar -xvf $HOME/homebrew/plugins/decky-rifm/bin/piper_linux_x86_64.tar.gz -C $HOME/homebrew/plugins/decky-rifm/bin
echo "LOG: Extracted piper_linux_x86_64.tar.gz."

echo "LOG: Removing /tmp/decky-rifm.zip..."
sudo rm /tmp/decky-rifm.zip
echo "LOG: Removed /tmp/decky-rifm.zip."

echo "LOG: Starting plugin_loader service..."
sudo systemctl start plugin_loader
echo "LOG: Started plugin_loader service."

echo "LOG: Setting permissions for decky-rifm..."
sudo chmod -R 777 $HOME/homebrew/plugins/decky-rifm
echo "LOG: Permissions set."

echo "LOG: DECKY-RIFM IS INSTALLED."

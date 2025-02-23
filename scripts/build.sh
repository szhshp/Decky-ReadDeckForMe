# Ensure the script is run from [ the root of the project ], not from the /scripts directory
pnpm run build

timestamp=$(date +"%Y%m%d%H%M%S")
filname="decky-rifm-debug.zip"


rm -r decky-rifm-debug
mkdir -p decky-rifm-debug/dist

cp -r dist/* decky-rifm-debug/dist
cp package.json decky-rifm-debug/
cp plugin.json decky-rifm-debug/
cp main.py decky-rifm-debug/ 2>/dev/null || :
cp README.md decky-rifm-debug/ 2>/dev/null || :
cp LICENSE decky-rifm-debug/ 2>/dev/null || cp LICENSE.md decky-rifm-debug/ 2>/dev/null || :

zip -r $filname decky-rifm-debug

scp $filname deck@192.168.1.9:~/_PLUGIN_DEBUG/${filename}


# ssh deck@192.168.1.9 "cd /home/deck/_PLUGIN_DEBUG; unzip -o PLUGIN.zip -d /home/deck/homebrew/plugins"

rm $filname
rm -r decky-rifm-debug
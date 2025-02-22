# Ensure the script is run from [ the root of the project ], not from the /scripts directory
pnpm run build

cd ..

timestamp=$(date +"%Y%m%d%H%M%S")
filname="PLUGIN.zip"

echo "Creating archive $filname"
zip -r $filname decky-rifm \
  -x "decky-rifm/node_modules/*" \
  "decky-rifm/.git/*" \
  "decky-rifm/.gitignore" \
  "decky-rifm/.gitattributes" \
  "decky-rifm/src" \
  "decky-rifm/.gitmodules"

scp $filname deck@192.168.1.9:~/_PLUGIN_DEBUG/${filename}
rm $filname


ssh deck@192.168.1.9 "cd /home/deck/_PLUGIN_DEBUG; unzip -o PLUGIN.zip -d /home/deck/homebrew/plugins"

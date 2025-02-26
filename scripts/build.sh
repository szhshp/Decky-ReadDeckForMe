# Ensure the script is run from the root of the project, not from the /scripts directory
pnpm run build

# Generate a timestamp for the filename
timestamp=$(date +"%Y%m%d%H%M%S")
# Define the filename for the zip file
filname="decky-rifm.zip"

# Remove any existing decky-rifm directory
rm -r decky-rifm

mkdir -p decky-rifm/dist
cp -r dist/* decky-rifm/dist
mkdir -p decky-rifm/bin
cp -r bin/* decky-rifm/bin

# Copy essential files to the new directory
cp package.json decky-rifm/
cp plugin.json decky-rifm/
cp main.py decky-rifm/ 2>/dev/null || :
cp README.md decky-rifm/ 2>/dev/null || :
# Copy the LICENSE file, handling different possible filenames
cp LICENSE decky-rifm/ 2>/dev/null || cp LICENSE.md decky-rifm/ 2>/dev/null || :

# Create a zip file of the new directory
zip -r $filname decky-rifm

# Securely copy the zip file to the remote server
scp $filname deck@192.168.1.10:/tmp/decky-rifm.zip

# Clean up by removing the local zip file and directory
rm $filname
rm -r decky-rifm
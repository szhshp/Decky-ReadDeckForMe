
# Decky Plugin - ReadItForMe 

This is a personal use decky plugin to read the text of your latest screenshot.

## Screenshots

(TODO)

## Development ENV Setup

1. Set up SSH to login without a password (using RSA).
2. Run `pnpm i` to install dependencies.
3. Run `/script/setup.sh` to build, zip, and ship the plugin to Decky.
4. Install the plugin in Decky-Loader in Dev mode.
5. Once you see `decky-rifm` in `/homebrew/plugins` in Decky-Loader, you can start developing the plugin.
6. Change the permissions of that folder: `sudo chmod -R 777 /decky-rifm` to allow overwriting files in that folder.
7. Make changes in the code, both frontend and backend.
8. Run `/script/build.sh` again to see the changes in Decky-Loader (you may need to reload or click the reinstall button in Decky-Loader).


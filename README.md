# Decky Plugin - ReadItForMe 

> Under Development, but feel free to try it out!

A personal Decky plugin to read the text from your latest screenshot.

## Screenshots

[Demo(Youtube)](https://www.youtube.com/watch?v=fjsc5IqgmzU?si=0S-l1QOr71csefn8)
[![YouTube](http://i.ytimg.com/vi/fjsc5IqgmzU/hqdefault.jpg)](https://www.youtube.com/watch?v=fjsc5IqgmzU)
## Dev Guide

1. Set up SSH for passwordless login (using RSA).
2. Run `pnpm install` to install dependencies.
3. Make your code changes.
4. Run `task:build` to build the project and `task:copyzip` to transfer the zip file to your Deck.
5. Run `script/deploy.sh` on your Deck to install the plugin.


### Features

- [x] Add a folder selector to choose where screenshots are saved
- [x] Add a button to download language models
- [x] Add Chinese Support
- [x] Check Model File Integrity
- [ ] Add stop read button
- [ ] Publish to the Decky Store

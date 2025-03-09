# Read Deck For Me

A Decky plugin to read the screen for you.

## Features

- Read the text from your latest screenshot.
- Download models for offline use.
- Support for English and Chinese.


## Installation


1. [**Install Decky-Loader**](https://github.com/SteamDeckHomebrew/decky-loader).
2. Toggle **Developer Mode** and install the plugin from the **Decky Settings**.

> Install from Decky Store will be available soon.

## Screenshots

[Demo(Youtube)](https://www.youtube.com/watch?v=fjsc5IqgmzU?si=0S-l1QOr71csefn8)
[![YouTube](http://i.ytimg.com/vi/fjsc5IqgmzU/hqdefault.jpg)](https://www.youtube.com/watch?v=fjsc5IqgmzU)

## Dev Guide

1. Set up SSH for passwordless login (using RSA).
2. Run `pnpm install` to install dependencies.
3. Make your code changes.
4. Run `task:build` to build the project and `task:copyzip` to transfer the zip file to your Deck.
5. Run `script/deploy.sh` on your Deck to install the plugin.


### TODO

- [x] Add a folder selector to choose where screenshots are saved
- [x] Add a button to download language models
- [x] Add Chinese Support
- [x] Check Model File Integrity
- [ ] Upload a video demo for the plugin
- [ ] Add stop read button
- [ ] Voice Speed Control
- [ ] Publish to the Decky Store

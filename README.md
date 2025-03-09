# Read Deck For Me

A Decky plugin to read the screen for you.

## Features

- Read the text from your latest screenshot.
- Download models for offline use.
- Support for English and Chinese.



## Demo

### Main Demo

>[Youtube](http://www.youtube.com/watch?v=91gW60wfL9I)

[![Main Demo](http://img.youtube.com/vi/91gW60wfL9I/0.jpg)](http://www.youtube.com/watch?v=91gW60wfL9I "Main Demo")

### Game Demo

>[Youtube](http://www.youtube.com/watch?v=cFGJLdHcK8o)

[![Game Demo](http://img.youtube.com/vi/cFGJLdHcK8o/0.jpg)](http://www.youtube.com/watch?v=cFGJLdHcK8o "Game Demo")

## Installation


1. [**Install Decky-Loader**](https://github.com/SteamDeckHomebrew/decky-loader).
2. Toggle **Developer Mode** and install the plugin from the **Decky Settings**.

> Install from Decky Store will be available soon.


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

Moderator to Streamer Live TTS
==============================

* Moderator Client
  * Minimal UI - tkinter
  * One line text entry and one button
  * Hits a server endpoint with a single line of encrypted text

* Streamer Client
  * HTTP server, intent to reverse proxy to the client from a gateway server
  * sends line of text through mimic tts to play as a system sound

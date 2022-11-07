Moderator to Streamer Live TTS
==============================

* Moderator Client
  * Minimal UI - possibly Tkinter, possibly QT
  * One line text entry and one button
  * Hits a server endpoint with a single line of text

* Orchestration Server
  * No web interface?  Maybe web interface? Maybe web interface instead of Moderator client?
  * accept a line of text on an endpoint, passes it along as SSE to streamer client

* Streamer Client
  * Waits on SSE
  * sends line of text through mimic tts to play as a system sound

* Profit
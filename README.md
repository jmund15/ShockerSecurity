# Shocker Security (Senior Design Project)

By Jacob Mund and Tina Leung

## Process Overview
1. Collect initial accepted faces
2. Store Pickle Data as BLOB within SQLite database
3. Run the 24/7 video stream. This will output the video output from the pi, either to a UDP socket or Ffmpeg
4. Match frames from video stream with encoded faces from database.
5. If a face exists that doesn't match with faces in database, save frame and send picture to user.
6. (Optional) User could have option to add unknown face to accepted.

## Process Questions
* User should be able to stream video from their device from anywhere (with proper authentication), how do we achieve this
* User should be able to add or remove faces from database, and have running security system update while still streaming. 
# Indoor Localisation Accuracy

## Overview

This module is used to test the accuracy of indoor localisation in a general way (more than just the ML model). Even if multiple methods such as WiFi, GPS, accelerometer etc are combined to improve performance, this module can still test the estimated locations.

The testing method relies on a computer vision technique and ArUCo markers to accurately determine test user's location. This test location can then be compared to the location estimated by the localisation app.

Wondering why this computer vision technique can't be used by the localisation app itself? Because the app user might not want to wear an aruco marker at all times or want to be the subject of the camera. But the person testing their app shouldn't mind 😀.

## Method

1. Generate ArUCo locations from camera video using `ArUCo-markers-cv-localisation-method` module

   Read the `ArUCo-markers-cv-localisation-method/README.md` for more info

   For an example video, see `Demo 1`

   You can use the ['find location' page on the testing app](https://indoor-localisation-accuracy-testing-tool.vercel.app/find-position) to find the camera translation (in metres) from the building origin.

2. Record Localisation App Location Predictions (see `Demo 2`)
3. Input both sets of locations to [testing app](https://indoor-localisation-accuracy-testing-tool.vercel.app/) (see `Demo 3`)
4. Save test results

## Demo

https://github.com/user-attachments/assets/aa7c1bc2-a23f-4203-936e-fb4d93584d94

[app]

# (str) Title of your application
title = Euro Predictions

# (str) Package name
package.name = europredictions

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1

[android]

# (bool) Accept SDK license without prompt
accept_sdk_license = True

# (int) Target Android API
api = 33

# (int) Minimum API required
minapi = 21

# (str) Android NDK version to use
ndk = 25b

# (str) Android SDK version to use
sdk = 33

# (list) List of architectures to build for
android.archs = arm64-v8a

          

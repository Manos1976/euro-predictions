[app]
title = Euro Predictions
package.name = europredictions
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
accept_sdk_license = True
api = 33
minapi = 21
ndk = 25b
sdk = 33
archs = arm64-v8a

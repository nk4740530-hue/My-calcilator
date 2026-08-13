[app]

title = My Calculator
package.name = mycalculator
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv

version = 1.0

requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.1

orientation = portrait
fullscreen = 0

android.api = 34
android.minapi = 21
android.arch = arm64-v8a
android.accept_sdk_license = True

p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 1

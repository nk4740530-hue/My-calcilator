[app]

title = Nivas Math Solver
package.name = nivasmathsolver
package.domain = com.nivaskumar

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0.0

requirements = python3==3.14.2, kivy, sympy


orientation = portrait
fullscreen = 0

# Play Store के लिए current Android target
android.api = 36
android.minapi = 24
android.ndk = 29

android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET

# Release/Play settings
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1

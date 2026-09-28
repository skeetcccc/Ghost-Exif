# 🛡️ Anti-OSINT Metadata Spoofer CLI

A lightweight CLI tool written in Python designed to enhance operational security (OpSec) and counter OSINT reconnaissance by injecting randomized, fake EXIF metadata (GPS location, camera specifications, capture date, and editing software) into JPG/JPEG images.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🚀 Features

 **Anti-OSINT GPS Spoofing:** Generates fake, randomized geolocation coordinates.
 **Hardware Profile Spoofing:** Injects metadata matching high-end cameras and smartphones (Canon EOS 5D Mark IV, Nikon D850, iPhone 15 Pro, Pixel 8 Pro, Fujifilm X-T5).
 **Time Offset Injection:** Modifies original creation timestamps to random dates in the past.
 **Batch Processing:** Seamlessly handles single image files or entire directory trees.
 **Interactive Terminal UI:** Built with `rich` featuring an ASCII banner, progress bar, and automatic quote-stripping for drag-and-drop terminal usage.

---

## 🛠️ System Requirements

 **Operating System:** Linux (Fedora/Debian/Arch), macOS, or Windows
 **Python:** Version `3.8` or higher
 **Package Manager:** `pip`

---

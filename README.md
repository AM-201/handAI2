# handAI2

Real-time AI hand gesture recognition and ESP32 control system using MediaPipe, OpenCV, MQTT, Flask, and Python.

---

## Overview

handAI2 is a real-time embedded AI system that detects hand gestures using a laptop camera and translates them into MQTT commands that control LEDs connected to an ESP32.

The system also includes a live Flask dashboard with:

- Real-time camera stream
- Gesture visualization
- MQTT monitoring
- ESP32 status feedback
- Serial log display

This project combines:

- Computer Vision
- Embedded Systems
- MQTT Networking
- Real-Time Processing
- Human-Machine Interfaces (HMI)

---

## Demo

### Gestures

| Open Hand                                 | Fist                             | Peace Sign                                  |
| ----------------------------------------- | -------------------------------- | ------------------------------------------- |
| ![Open Hand](Images_and_GIF/OpenHand.jpg) | ![Fist](Images_and_GIF/Fist.jpg) | ![Peace Sign](Images_and_GIF/PeaceSign.jpg) |

---

### System Demo Video

![Demo](Images_and_GIF/handAI2_VID.mp4)

---

## Features

- Real-time hand tracking using MediaPipe
- Gesture recognition system
- MQTT publish/subscribe communication
- ESP32 LED control
- Live Flask dashboard
- MJPEG live video streaming
- Bidirectional communication
- Expandable architecture
- Modular codebase

---

## Supported Gestures

| Gesture     | MQTT Payload | ESP32 Action |
| ----------- | ------------ | ------------ |
| Open Hand   | G            | Green LED ON |
| Closed Fist | R            | Red LED ON   |
| Peace Sign  | W            | White LED ON |

---

## System Architecture

```text
Laptop Camera
      ↓
OpenCV Frame Capture
      ↓
MediaPipe Hand Tracking
      ↓
Gesture Recognition Logic
      ↓
MQTT Publish
      ↓
MQTT Broker
      ↓
ESP32 Subscriber
      ↓
LED Control

ESP32
      ↓
MQTT Status Feedback
      ↓
Flask Dashboard
      ↓
Browser Interface
```

## Usage

## how to run locally

```bash
# 1. Clone repository
git clone https://github.com/AM-201/handAI2.git
cd handAI2

# 2. Install required libraries
pip install -r requirements.txt

# run system
python main.py

# Open dashboard
http://127.0.0.1:5000



```

# AI-Based Assistive Navigation System

A real-time, low-cost AI vision assistant designed to help visually impaired individuals navigate their surroundings. The system uses a webcam or pre-recorded video to detect objects, estimate relative depth, recognize text, and provide prioritized audio guidance.

## Features

* **Object Detection** — Detects objects and potential obstacles using YOLOv8.
* **Depth Estimation** — Estimates relative depth using Depth Anything to identify objects that may pose an immediate collision risk.
* **Text Recognition (OCR)** — Detects and reads visible text and signs using EasyOCR.
* **Context-Aware Navigation** — Combines detection and depth information to filter visual noise and prioritize important events.
* **Text-to-Speech (TTS)** — Converts navigation instructions into spoken audio for hands-free use.

---

## 💻 Windows Setup

### 1. Prerequisites

Install the following:

* **Python:** 3.9, 3.10, or 3.11
* **Git:** Optional, if cloning the repository
* **Webcam:** Required for live inference
* **Speakers or headphones:** Required for audio guidance

Download Python from the [official Python website](https://www.python.org/downloads/).

> **Important:** During Python installation, enable **Add Python to PATH**.

---

### 2. Clone or Open the Project

If you are using Git:

```cmd
git clone <repository-url>
cd ml-project
```

Otherwise, open Command Prompt or PowerShell inside the project directory.

---

### 3. Create a Virtual Environment

Create an isolated Python environment for the project:

```cmd
python -m venv venv
```

---

### 4. Activate the Virtual Environment

#### Command Prompt

```cmd
venv\Scripts\activate
```

#### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 5. Install Dependencies

Make sure the virtual environment is activated, then run:

```cmd
pip install -r requirements.txt
```

---

## 🚀 Optional: NVIDIA GPU Acceleration

If your system has a compatible NVIDIA GPU, PyTorch can use CUDA to significantly improve inference performance.

After installing the project dependencies, install the appropriate CUDA-enabled PyTorch build.

For the CUDA 12.1 build:

```cmd
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

> **Note:** The correct PyTorch/CUDA combination depends on your GPU, driver, and project requirements. If the command above is incompatible with your system, check the official [PyTorch installation instructions](https://pytorch.org/get-started/locally/).

---

# ▶️ Running the Application

## Live Webcam

By default, the application can process frames from the computer's webcam.

Make sure your webcam is connected and your speakers or headphones are enabled.

Run:

```cmd
python main.py
```

A window should open showing the camera feed with AI-generated detections and visual overlays.

To stop the application:

1. Click the video window.
2. Press **`q`**.

---

## Test Using a Video File

The system can also process a pre-recorded video.

Open `main.py` and configure the video source:

```python
processor.process_video(
    source_path="my_test_video.mp4",
    output_path="output.mp4"
)
```

Then run:

```cmd
python main.py
```

The processed video will be saved as:

```text
output.mp4
```

---

# 📁 Project Structure

```text
ml-project/
│
├── main.py
├── video_processor.py
├── config.py
├── detector.py
├── depth.py
├── ocr.py
├── navigation.py
├── speech.py
├── utils.py
├── requirements.txt
└── README.md
```

### File Descriptions

| File                 | Purpose                                                     |
| -------------------- | ----------------------------------------------------------- |
| `main.py`            | Application entry point                                     |
| `video_processor.py` | Coordinates the AI pipeline and processes video frames      |
| `config.py`          | Stores thresholds, cooldown values, and model configuration |
| `detector.py`        | YOLOv8 object detection                                     |
| `depth.py`           | Monocular depth estimation using Depth Anything             |
| `ocr.py`             | Text detection and recognition using EasyOCR                |
| `navigation.py`      | Determines which objects or events are relevant to the user |
| `speech.py`          | Handles text-to-speech output using pyttsx3                 |
| `utils.py`           | Utility functions for visualization and frame processing    |

---

# 🧠 Processing Pipeline

The system processes the environment approximately as follows:

```text
Camera / Video
      │
      ▼
┌─────────────────┐
│  Video Frame    │
└────────┬────────┘
         │
         ├───────────────┐
         ▼               ▼
┌──────────────┐  ┌──────────────┐
│ YOLOv8       │  │ Depth        │
│ Detection    │  │ Anything     │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │ Navigation      │
       │ Engine          │
       └────────┬────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
   Important         Not Relevant
     Event               │
        │                └── Ignore
        ▼
┌─────────────────┐
│ Text / OCR      │
│ (when enabled)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Text-to-Speech  │
└────────┬────────┘
         │
         ▼
    Audio Guidance
```

The navigation engine is responsible for reducing unnecessary speech and prioritizing information that is most useful for immediate navigation.

---

# ⚙️ Performance Tuning

Running object detection, depth estimation, and OCR simultaneously can be computationally expensive, especially on CPU-only systems.

### Reduce Processing Frequency

If the video is lagging, increase the cooldown value in `config.py`.

For example:

```python
COOLDOWN_SECONDS = 4.0
```

or:

```python
COOLDOWN_SECONDS = 5.0
```

A higher cooldown reduces how frequently navigation information is generated and spoken.

### Disable OCR

OCR is one of the more computationally expensive components.

If text recognition is not required, disable it in `main.py`:

```python
run_ocr = False
```

This can improve performance considerably.

### Use GPU Acceleration

For systems with a compatible NVIDIA GPU, configuring PyTorch with CUDA can substantially reduce inference time compared with CPU-only execution.

---

# 🔊 Troubleshooting

## Application Is Slow or Laggy

Running multiple AI models on a CPU can cause low FPS and delayed responses.

Try:

* Increasing `COOLDOWN_SECONDS`.
* Disabling OCR with `run_ocr=False`.
* Using a smaller/faster YOLO model if configured by the project.
* Using a compatible NVIDIA GPU with CUDA acceleration.
* Reducing the input video resolution.

---

## No Audio

Check that:

* System volume is enabled.
* The correct audio output device is selected.
* Speakers or headphones are connected.
* The application is running inside the activated virtual environment.

On Windows, `pyttsx3` normally uses the native **SAPI5** speech engine.

---

## `ModuleNotFoundError`

Make sure the virtual environment is activated:

```cmd
venv\Scripts\activate
```

Then reinstall the dependencies:

```cmd
pip install -r requirements.txt
```

You can verify that Python is using the virtual environment with:

```cmd
where python
```

The displayed path should point to the project's `venv` directory.

---

# ⚠️ Limitations

This system is intended as an **assistive prototype**, not a replacement for a mobility aid, trained guide, or independent navigation technology.

Potential limitations include:

* Depth estimation provides **relative** depth rather than guaranteed physical distance.
* Object detection can miss objects or produce incorrect classifications.
* OCR performance depends on lighting, text size, orientation, and image quality.
* Processing multiple AI models simultaneously can introduce latency.
* Audio guidance may become less reliable in noisy environments.
* The system may not correctly understand every complex environmental situation.

Users should not rely exclusively on the system for safety-critical navigation.

---

# 🛠️ Technology Stack

* **Python**
* **YOLOv8** — Object Detection
* **Depth Anything** — Monocular Depth Estimation
* **EasyOCR** — Optical Character Recognition
* **OpenCV** — Video and image processing
* **pyttsx3** — Text-to-Speech
* **PyTorch** — Deep Learning Framework

---

# 📌 Future Improvements

Possible future improvements include:

* Real-world distance calibration.
* Better obstacle prioritization.
* Object tracking between frames.
* Improved scene understanding.
* More efficient model scheduling.
* Voice commands and user interaction.
* GPS-based outdoor navigation.
* Support for mobile or edge devices.
* Hardware integration with wearable cameras and audio devices.


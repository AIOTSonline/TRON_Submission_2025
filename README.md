# AIOTS x TRON 2025 - Visual IDE for Micro:bit Development

<p align="center">
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white&borderRadius=10" alt="C++" style="border-radius: 10px;">
  <img src="https://img.shields.io/badge/Micro:bit-00ED00?style=for-the-badge&logo=microbit&logoColor=white&borderRadius=10" alt="Micro:bit" style="border-radius: 10px;">
  <img src="https://img.shields.io/badge/μT_Kernel-3.0-orange?style=for-the-badge&borderRadius=10" alt="μT Kernel 3.0" style="border-radius: 10px;">
</p>

A visual programming environment that enables drag-and-drop C++ code blocks with AI-powered code refinement for Micro:bit microcontroller compatibility.

## Overview

Our project provides an intuitive visual interface where users can construct C++ programs by dragging and dropping code blocks. The integrated GenAI system analyzes and refines the code to ensure compatibility with the BBC Micro:bit microcontroller platform.

## Features

* **Visual Drag-and-Drop Interface**: Intuitive block-based programming for C++ code
* **AI-Powered Code Analysis**: Automatic code refinement using Gemini AI
* **Micro:bit Optimization**: Ensures code compatibility with Micro:bit hardware constraints
* **Real-time Feedback**: Instant code validation and suggestions

## Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: FastAPI (Python)
* **AI Integration**: Google Gemini API
* **Target Platform**: BBC Micro:bit

## Prerequisites

* Python 3.7+
* Node.js (for Live Server)
* Google Gemini API Key
* Modern web browser
* BBC Micro:bit V3

## Setup Instructions

### 1. Install Dependencies

Navigate to the `Code_Correction_Part` folder and install required Python packages:

```bash
cd Code_Correction_Part
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `Code_Correction_Part` directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

To obtain a Gemini API key, visit [Google AI Studio](https://aistudio.google.com/app/apikey).

### 3. Run the Backend

Start the FastAPI server with Uvicorn (from within `Code_Correction_Part`):

```bash
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`.

### 4. Launch the Frontend

Navigate to the `demo` folder and open `index.html` using Live Server:

* If using VS Code, install the Live Server extension
* Right-click on `index.html` and select "Open with Live Server"
* The application will open in your default browser

## Project Structure

```
TRON-2025/
├── Code_Correction_Part/
│   ├── main.py              # FastAPI backend
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (create this)
└── demo/
    └── index.html           # Frontend application
```

## Usage

1. Launch both the backend server and frontend application
2. Drag and drop C++ code blocks to build your program
3. The AI will automatically analyze and refine your code for Micro:bit compatibility
4. Review suggestions and finalize your code
5. Deploy to your Micro:bit device

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Acknowledgments

* Built for TRON 2025
* Powered by Google Gemini AI
* Supports BBC Micro:bit platform

## Support

For questions or issues, please open an issue in the GitHub repository.

## Special Thanks

* The developers of [Blockly](https://github.com/google/blockly)



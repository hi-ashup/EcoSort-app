<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/hi-ashup/EcoSort-app/blob/main/asset/ecoSort-app.png" />
</div>

# EcoSort: Intelligent Waste Classifier

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Material UI](https://img.shields.io/badge/MUI-%230081CB.svg?style=for-the-badge&logo=mui&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)

## 🌿 Core Objective
EcoSort is a high-performance, aesthetically futuristic web application designed to combat waste mismanagement. Using advanced computer vision and the Gemini 3 Flash model, it classifies waste items in real-time and provides expert-level disposal, recycling, and upcycling intelligence.

**Live Demo**: [EcoSort Live Web Application](https://eco-sort-app-teal.vercel.app/)

---

## 🚀 Key Features

*   **Neural Scanner (Optical HUD)**: Real-time molecular-style analysis via live camera feed or high-resolution image uploads.
*   **Gemini 3 Integration**: Leverages the latest GenAI models for rapid object recognition and precise material composition breakdown.
*   **Classification Node**: Provides technical ratings on recyclability, environmental impact, and visual mapping to global sorting standards (Color-coded Bin mapping).
*   **Material Intel**: A deep-dive diagnostic into the chemical/material makeup of items using animated detection strength indicators.
*   **Disposal Protocol**: Professional step-by-step preparation guides (e.g., "Rinse, Dry, Compress") to ensure zero-contamination recycling.
*   **Upcycling Lab**: Innovative "Best-out-of-waste" project generation to promote a circular economy.

---

## 🛠️ Technical Stack

*   **Frontend**: React 19 + TypeScript
*   **UI Framework**: Material UI (MUI) v6 with custom Emerald-Dark theme.
*   **AI Engine**: Google GenAI SDK (@google/genai)
*   **Icons**: Lucide React
*   **Styling**: Emotion Styled Components + CSS3 Keyframe Animations

---

## 💻 Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/hi-ashup/EcoSort-app.git
    cd ecosort
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    ```

3.  **Environment Configuration**:
    Create a `.env` file in the root directory and add your Gemini API Key:
    ```env
    API_KEY=your_google_gemini_api_key_here
    ```

4.  **Run Development Server**:
    ```bash
    npm run dev
    ```

---

## 🧪 System Diagnostics

### Neural Response Schema
The system interprets visual data and returns a structured diagnostic report including:
- **Recyclability Rating**: High, Moderate, or None.
- **Environmental Impact**: Detailed ecological footprint analysis.
- **Sorting Protocol**: Identification of the correct global bin color (Green, Blue, Yellow, Red, Black).

---

## 🔑 Security & API
This application utilizes the Google Gemini API. Ensure your API key is restricted to the "Generative Language API" in the [Google Cloud Console](https://console.cloud.google.com/) for production deployments.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed with a commitment to a zero-waste future.*
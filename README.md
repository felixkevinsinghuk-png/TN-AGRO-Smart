# 🌱 AGRO_Smart

AGRO_Smart is an AI-powered agricultural assistant designed to help farmers and gardeners instantly detect plant diseases. By simply uploading an image of a plant leaf, the internal AI engine uses a custom Convolutional Neural Network (CNN) trained on PyTorch to identify the disease and recommend actionable prevention steps and supplements.

## 🌟 Key Features
- **Instant AI Diagnosis**: Uses a deep learning model to accurately identify over 39 classes of plant diseases and healthy leaves.
- **Actionable Recommendations**: Provides disease descriptions, prevention steps, and links to recommended supplements.
- **Premium Glassmorphism UI**: A sleek, dark-mode frosted glass interface for an intuitive and modern user experience.
- **Secure Authentication**: Includes a dedicated login/registration portal.

## 🛠️ Tech Stack
- **Machine Learning**: PyTorch, Torchvision, NumPy, Pandas, scikit-learn
- **Backend Framework**: Flask (Python)
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism Design System), JavaScript, Bootstrap 5
- **Authentication**: Firebase (Standalone Auth App)

## 📁 Project Structure
- `/Plant-Disease-Detection-main`: The core ML application, containing the PyTorch models, Jupyter Notebooks for custom training, and the Flask deployed web app.
- `/login`: The standalone Firebase authentication portal.
- `/Flask_AUTH_with_Mysql-main`: Alternative SQL-based authentication implementation.
- `/SignUP-SignIn-Form-with-connection-to-FIrebase-main`: Additional Firebase auth templates.

## 🚀 How to Run Locally
1. Clone the repository to your local machine.
2. Navigate to the main Flask application folder:
   ```bash
   cd "Plant-Disease-Detection-main/Flask Deployed App"
   ```
3. Set up a Python virtual environment and install the required dependencies (PyTorch, Flask, Pandas, etc.).
4. Start the Flask server:
   ```bash
   python app.py
   ```
5. Open your browser and navigate to `http://127.0.0.1:5000/`.

## 🙏 Acknowledgements

This project was inspired by the original Plant Disease Detection work by:

> **[@manthan89-py](https://github.com/manthan89-py)** — [Plant-Disease-Detection](https://github.com/manthan89-py/Plant-Disease-Detection)

The architecture concept, dataset pipeline, and core AI engine idea draw inspiration from their excellent open-source contribution. AGRO_Smart builds upon this foundation with a new premium UI/UX, extended features, and a Firebase-based authentication system.

---
*Developed by Felix Kevin.*

# 🫀 DiagnoAI - Heart Disease Prediction  

## 📌 Description  
**DiagnoAI** is a Machine Learning-based application designed to assist in predicting heart disease based on user health data.  
The application takes input such as age, gender, blood pressure, cholesterol, fasting blood sugar, and chest pain symptoms.  

The system uses multiple machine learning models:  
1. **Decision Tree**  
2. **K-Nearest Neighbors (KNN)**  
3. **Support Vector Machine (SVM)**  

Each model provides its own prediction, allowing users to compare results across different algorithms.  

---

## 🚀 Example Output  
For a given input, the prediction results will look like this:  

```
Bot: Prediction :
1. Decision Tree: Normal
2. K-Nearest Neighbors: Heart Disease
3. Support Vector Machine: Heart Disease
```

---

## 📂 Project Structure  
```
DiagnoAI/
│── app.py                # Main Flask / Streamlit app
│── models/
│   ├── decision_tree.pkl  # Trained Decision Tree model
│   ├── knn.pkl            # Trained KNN model
│   └── svm.pkl            # Trained SVM model
│── static/                # CSS / JS files
│── templates/             # HTML UI files
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```

---

## ⚙️ How to Run  

1. **Clone Repository**
   ```bash
   git clone https://github.com/juanariviano/DiagnoAI.git
   cd DiagnoAI
   ```

2. **Create Virtual Environment (Optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   Then open your browser at `http://127.0.0.1:5000`

---

## 📊 Dataset  
The models were trained on a heart disease dataset containing features such as:  
- Age  
- Gender  
- Blood Pressure  
- Cholesterol  
- Fasting Blood Sugar  
- Chest Pain  
- etc.  

---

## 🛠 Technologies Used  
- **Python 3.x**  
- **Flask** / Streamlit (for the web app)  
- **Scikit-learn** (Decision Tree, KNN, SVM)  
- **HTML, CSS, JavaScript** (UI/Frontend)  

---

## 📌 Notes  
- This application is an **educational prototype** and **does not replace professional medical diagnosis**.  
- The prediction results should only be used as an early reference, not a final decision.  

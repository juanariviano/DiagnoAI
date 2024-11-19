from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# Inisialisasi aplikasi Flask dan SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Rute untuk melayani file dari folder assets
@app.route('/assets/favicon.ico')
def serve_favicon():
    return send_from_directory('assets', 'favicon.ico')


# Load dan preprocessing dataset
url = 'https://drive.google.com/uc?export=download&id=1RdNi0rwNyYRchBWSfuS0mTJuM-vV_kk4'
df = pd.read_csv(url, index_col=0)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('user_message')
def handle_message(data):
    # Contoh hasil prediksi dari model
    predictions = {
        'Decision Tree': 'Normal',
        'K-Nearest Neighbors': 'Jantung',
        'Support Vector Machine': 'Jantung'
    }
    
    # Kirim data sebagai JSON tanpa mengonversinya ke string
    socketio.emit('bot_response', {'message': predictions})



# Inisialisasi LabelEncoder untuk kolom kategori
jk_encoder, nd_encoder, s_encoder = LabelEncoder(), LabelEncoder(), LabelEncoder()

# Inisialisasi label untuk kolom kategori
df['jenis kelamin'] = jk_encoder.fit_transform(df['jenis kelamin'])
df['nyeri dada'] = nd_encoder.fit_transform(df['nyeri dada'])
df['slope'] = s_encoder.fit_transform(df['slope'])
df['diagnosis'] = df['diagnosis'].map({'Jantung': 1, 'Normal': 0})

# Memisahkan fitur (X) dan target (y)
X, y = df.drop(columns=['diagnosis']), df['diagnosis']
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Inisialisasi model-model
models = {
    "Decision Tree": DecisionTreeClassifier(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Support Vector Machine": SVC(kernel='linear')
}

# Melatih model dengan data latih
for model_name, model in models.items():
    model.fit(X_train, y_train)

# Fungsi untuk transformasi label yang aman dengan fallback jika label tidak dikenal
def safe_transform(encoder, value, default):
    try:
        return encoder.transform([value])[0]
    except ValueError:
        # Jika terjadi ValueError (misal label tidak ditemukan), gunakan default
        print(f"Label '{value}' tidak ditemukan. Menggunakan nilai default '{default}'.")
        return encoder.transform([default])[0]

# Handler chatbot untuk prediksi
# Fungsi untuk menangani pesan dari pengguna
@socketio.on('user_message')
def handle_message(message):
    try:
        # Parsing data input dari pengguna
        data = message.get('data', {})
        
        # Menerima data input dan memastikan nilai sesuai dengan label yang valid
        new_data = pd.DataFrame({
            'usia': [data.get('usia')],
            'jenis kelamin': [safe_transform(jk_encoder, data.get('jenis_kelamin', 'Laki-laki'), 'Laki-laki')],
            'nyeri dada': [safe_transform(nd_encoder, data.get('nyeri_dada', 'Asymptomatic'), 'Asymptomatic')],
            'trestbps': [data.get('trestbps')],
            'cholestoral': [data.get('cholestoral')],
            'fasting blood sugar': [data.get('fasting_blood_sugar')],
            'restecg': [data.get('restecg')],
            'denyut jantung': [data.get('denyut_jantung')],
            'exang': [data.get('exang')],
            'oldpeak': [data.get('oldpeak')],
            'slope': [safe_transform(s_encoder, data.get('slope', 'Upsloping'), 'Upsloping')],
            'ca': [data.get('ca')],
            'thalium': [data.get('thalium')]
        })

        # Standardisasi data input
        new_data_scaled = scaler.transform(new_data)

        # Mendapatkan prediksi dari setiap model
        predictions = {}
        for model_name, model in models.items():
            prediction = model.predict(new_data_scaled)
            result = "Normal" if prediction[0] == 0 else "Jantung"
            predictions[model_name] = result

        # Membuat format pesan yang lebih rapi
        # Membuat format pesan yang lebih rapi
        formatted_predictions = "Prediksi :\n"
        for idx, (model_name, result) in enumerate(predictions.items(), 1):
            formatted_predictions += f"{idx}. {model_name}: {result}\n"

        # Mengirim hasil prediksi kembali ke pengguna
        socketio.emit('bot_response', {'message': formatted_predictions})

    
    except Exception as e:
        socketio.emit('bot_response', {'message': f"Error: {str(e)}"})


# Menjalankan aplikasi
if __name__ == '__main__':
    socketio.run(app, debug=True)

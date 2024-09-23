from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import numpy as np
from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError

app = Flask(__name__)

# Load model
# Load model terlatih
model_path = 'model/model_bin.pkl'
print(f"Loading model from {model_path}")
model_bin = joblib.load(model_path)
print("Model loaded successfully")

# Load model kedua (model_multi)
model_multi_path = 'model/model_multi.pkl'
print(f"Loading model from {model_multi_path}")
model_multi = joblib.load(model_multi_path)
print("Model 2 loaded successfully")

try:
    check_is_fitted(model_bin)
    print("Model 1 is fitted and ready to use.")
    check_is_fitted(model_multi)
    print("Model 2 is fitted and ready to use.")
except NotFittedError as e:
    print(f"Model is not fitted: {e}")

# Load dataset
dataset_path = 'static/data/kdd_full.csv'
df = pd.read_csv(dataset_path, delimiter=';')

@app.route('/')
def home():
    data = df.head(25).to_html(classes='table table-striped', index=False)
    return render_template('index.html', table=data)

@app.route('/pengujian', methods=['GET', 'POST'])
def pengujian():
    prediction = None
    form_data = {}
    if request.method == 'POST':
        form_data = request.form.to_dict()
        features = [
            form_data['src_bytes'],
            form_data['dst_bytes'],
            form_data['duration'],
            form_data['dst_host_srv_count'],
            form_data['count'],
            form_data['dst_host_count'],
            form_data['dst_host_srv_serror_rate'],
            form_data['srv_serror_rate'],
            form_data['serror_rate'],
            form_data['dst_host_serror_rate'],
            form_data['logged_in'],
            form_data['num_root'],
            form_data['num_compromised'],
            form_data['dst_host_same_srv_rate'],
            form_data['same_srv_rate'],
            form_data['srv_rerror_rate'],
            form_data['rerror_rate'],
            form_data['dst_host_srv_rerror_rate'],
            form_data['dst_host_rerror_rate'],
            form_data['dst_host_diff_srv_rate']
        ]
        
        features = pd.DataFrame([features], columns=[
            'src_bytes', 'dst_bytes', 'duration', 'dst_host_srv_count', 'count',
            'dst_host_count', 'dst_host_srv_serror_rate', 'srv_serror_rate',
            'serror_rate', 'dst_host_serror_rate', 'logged_in', 'num_root', 'num_compromised',
            'dst_host_same_srv_rate', 'same_srv_rate', 'srv_rerror_rate', 'rerror_rate',
            'dst_host_srv_rerror_rate', 'dst_host_rerror_rate', 'dst_host_diff_srv_rate'
        ])
        features = features.astype(float)

        try:
            prediction = model_bin.predict(features)[0]
        except NotFittedError as e:
            prediction = f"Model is not fitted: {e}"

    return render_template('pengujian.html', prediction=prediction, form_data=form_data)

@app.route('/pengujian_multi', methods=['GET', 'POST'])
def pengujian_multi():
    prediction_multi = None
    form_data_multi = {}
    if request.method == 'POST':
        form_data_multi = request.form.to_dict()
        features_multi = [
            form_data_multi['src_bytes'],
            form_data_multi['dst_bytes'],
            form_data_multi['duration'],
            form_data_multi['count'],
            form_data_multi['dst_host_srv_count'],
            form_data_multi['dst_host_count'],
            form_data_multi['srv_count'],
            form_data_multi['hot'],
            form_data_multi['dst_host_srv_serror_rate'],
            form_data_multi['srv_serror_rate'],
            form_data_multi['serror_rate'],
            form_data_multi['dst_host_serror_rate'],
            form_data_multi['logged_in'],
            form_data_multi['num_root'],
            form_data_multi['num_compromised'],
            form_data_multi['dst_host_same_srv_rate'],
            form_data_multi['same_srv_rate'],
            form_data_multi['dst_host_same_src_port_rate'],
            form_data_multi['dst_host_diff_srv_rate'],
            form_data_multi['srv_rerror_rate']
        ]
        
        features_multi = pd.DataFrame([features_multi], columns=[
            'src_bytes', 'dst_bytes', 'duration', 'count', 'dst_host_srv_count',
            'dst_host_count', 'srv_count', 'hot', 'dst_host_srv_serror_rate',
            'srv_serror_rate', 'serror_rate', 'dst_host_serror_rate', 'logged_in',
            'num_root', 'num_compromised', 'dst_host_same_srv_rate', 'same_srv_rate',
            'dst_host_same_src_port_rate', 'dst_host_diff_srv_rate', 'srv_rerror_rate'
        ])
        features_multi = features_multi.astype(float)

        try:
            prediction_multi = model_multi.predict(features_multi)[0]
        except NotFittedError as e:
            prediction_multi = f"Model is not fitted: {e}"

    return render_template('pengujian_multi.html', prediction_multi=prediction_multi, form_data_multi=form_data_multi)

if __name__ == '__main__':
    app.run(debug=True)


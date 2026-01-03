from flask import Flask, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/vaccines', methods=['GET'])
def vaccines():
    return render_template('vaccines.html')

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html')

@app.route('/api/vaccines', methods=['GET'])
def get_vaccines():
    df = pd.read_csv(
        './data/country_vaccinations.csv',
        sep=';',
        engine='python',
        on_bad_lines='skip'
    )

    # ép kiểu object để pandas không tự xuất NaN đặc biệt
    for c in df.columns:
        df[c] = df[c].astype(object)

    # thay mọi NaN/NaT/inf bằng None
    df = df.where(pd.notnull(df), None)

    vaccines_list = df.to_dict(orient='records')
    print(">>> USING vaccine_app.py WITH NaN->None <<<")
    return jsonify(vaccines_list)


if __name__ == '__main__':
    app.run(debug=True, port=8080)

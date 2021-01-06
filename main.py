from flask import Blueprint, render_template, url_for, flash, redirect, jsonify, request
from backend.forms import register_account, classification_form
from backend.models import User, Classification
from flask_login import login_user, current_user, login_required
from backend.predict import predict_iris
from .models import db, Classification

import joblib

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main.route("/dashboard", methods=(['GET', 'POST']))
@login_required
def dashboard():
    avatar = url_for('static', filename='profile_img/' + current_user.avatar)
    return render_template('dashboard.html', avatar=avatar)


@main.route('/ajax', methods=(['GET', 'POST']))
@login_required
def list_ajax():
    return render_template('request.html')

# @main.route('/predict')
# @login_required
# def predict():
#     return render_template('form.html')


# @main.route('/predict', methods=(['POST', 'GET']))
# def predict_form():
#     if request.method == 'POST':
#         sepal_length = float(request.form['sepal_length'])
#         sepal_width = float(request.form['sepal_width'])
#         petal_length = float(request.form['petal_length'])
#         petal_width = float(request.form['petal_width'])

#         model_learning = joblib.load(
#             r"F:\MyFlask\Project1\backend\model\svm_model_iris.pkl")
#         result = model_learning.predict(
#             [[sepal_length, sepal_width, petal_length, petal_width]])
#         classification = result[0]
#         return render_template('form.html', result=classification, petal_width=petal_width, sepal_width=sepal_width,
#                                sepal_length=sepal_length,
#                                petal_length=petal_length)
#     else:
#         return render_template('form.html')


@main.route('/predict', methods=['POST'])
def predict_iris():

    if request.method == 'POST':
        sepal_length = float(request.form.get('sepal_length'))
        sepal_width = float(request.form.get('sepal_width'))
        petal_length = float(request.form.get('petal_length'))
        petal_width = float(request.form.get('petal_width'))

        model_learning = joblib.load(
            r"F:\MyFlask\Project1\backend\model\svm_model_iris.pkl")
        result = model_learning.predict(
            [[sepal_length, sepal_width, petal_length, petal_width]])
        classification = result[0]

        return jsonify({'result': classification, 'sepal_length': sepal_length, 'sepal_width': sepal_width, 'petal_length': petal_length, 'petal_width': petal_width})

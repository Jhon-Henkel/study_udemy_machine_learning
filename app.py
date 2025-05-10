from flask import Flask, request

App = Flask(__name__)

@App.route('/')
def home():
    return {'Response':'Ok'}

@App.route('/api/predictive')
def api_predictive():
    return {'Response':'Ok'}

if __name__ == "__main__":
    App.run(debug=True)

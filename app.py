from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    my_value = os.getenv('MY_SECRET')
    return f"The secret value is: {my_value}"

if __name__ == '__main__':
    app.run(debug=True)

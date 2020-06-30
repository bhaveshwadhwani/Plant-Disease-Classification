from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_mail import Mail
import os

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "thefarmerhelper@gmail.com",
    MAIL_PASSWORD = "farmer@123" 
)
mail = Mail(app)



@app.route('/')
def home():
	return render_template('index.html')

@app.route("/" ,methods = ["GET", "POST"])
def result():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join("static/upload", secure_filename(f.filename)))
		from src.predict import build
		filepath = os.path.join("static/upload", secure_filename(f.filename))
		result = build(filepath)
		st = "Your Predicted result is "
		result = st + str(result)
		print(result)
		return render_template("result.html", result=result)
	return render_template("index.html")

@app.route("/",methods=['GET','POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('Name')
        print(name)
        email = request.form.get('Email')
        message = request.form.get('Message')
        mail.send_message('New message from ' + email,
                      sender='thefarmerhelper@gmail.com',
                      recipients=['dmakwana503@gmail.com'],
                      body=message + " from " + name
                      )
    return render_template('index.html')

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=8080, debug=True)
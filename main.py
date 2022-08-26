from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL = os.getenv("EMAIL")
EMAIL2 = os.getenv("EMAIL2")
PAS = os.getenv("PAS")

app = Flask(__name__)
response = requests.get("https://api.npoint.io/9fee105de0092e5c521a")
response.raise_for_status()
print(response.status_code)
data = response.json()


@app.route("/")
def home():
    return render_template("index.html", jsondata=data)

@app.route("/about")
def about():
    return render_template("about.html")

# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

@app.route("/post/<blog_title>")
def show_post(blog_title):
    for post in data:
        if post["title"] == blog_title:
            blog_post = post
    return render_template("post.html", post=blog_post)

@app.route("/contact", methods=["POST", "GET"])
def receive_data():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(password=PAS, user=EMAIL)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL2,
                                msg=f"Subject: New form filled in! \n\n"
                                    f"{name} is trying to get in touch with you.\n"
                                    f"He/she left you a message:\n{message}\n"
                                    f"You can contact him/her writing an email to {email}\n"
                                    f"or calling this number: {phone}")
        return render_template("contact.html", m="post")
    else:
        return render_template("contact.html", m="get")



if __name__ == "__main__":
    app.run(debug=True)
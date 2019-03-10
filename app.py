from flask import Flask, render_template
from dbconnect import client

app = Flask(__name__)

# open connection
package = client.package

@app.route("/")
def web():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
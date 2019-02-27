from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

mars = mongo.db.mars
# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", python_dict=mars)


@app.route("/scrape")
def scraper():
    mars_data = scrape.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
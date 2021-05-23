from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import json

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    items = mongo.db.items.find_one()
    return render_template("index.html", items=items)


@app.route("/scrape")
def scraper():
    items = mongo.db.items
    items_data = scrape_mars.scrape()
    mongo.db.items.replace_one({}, items_data )
    #Fixes internal server error
    # items.replace_one({}, items_data, True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
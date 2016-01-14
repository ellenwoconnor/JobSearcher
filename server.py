from flask import Flask, request, render_template
from time import sleep
from JobSearcher import JobSearcher

app = Flask(__name__)

# app.secret_key = 'this-should-be-something-unguessable'


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/show_listings')
def retrieve_listings():

    location = request.args.get('location')
    print location
    is_partner = request.args.get('is_partner')
    print is_partner
    title = request.args.get('title')
    print title, type(title)
        # If they enter nothing? I think this would be an empty string, not None
        # Test to check

    jobs = JobSearcher(location, is_partner, title)
    listings = jobs.get_listings()

    return render_template('listings.html', listings=listings)

if __name__ == "__main__":
    app.run(debug=True)

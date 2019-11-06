import requests
from flask import Flask, Response, request

from flask import jsonify
import json

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error=None):
    """
    This is the error handler route. If it is 404, this will handle that
    :param error: for any specific error name
    :return: A response message of 404
    """
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/hotels/search', methods=["GET"])
def get_data():
    """
    This is the API I've designed that gets the request from 5 endpoints of hotel
    :return: returns a json response of the search result sorted in descending order based on ecstasy
    """
    providers = ['Expedia', 'Orbitz', 'Priceline', 'Travelocity', "Hilton"]
    results_to_providers = dict()

    try:
        results_to_providers["results"] = []

        for provider in providers:
            url = "http://localhost:9000/scrapers/" + provider
            json_data = json.loads(requests.get(url).content)   # The get request call
            results_to_providers["results"] += json_data["results"]
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException):
        not_found()

    # Here I are sorting the result in n * log(n)
    # Since I didn't get the result in sorted order, I had to explicitly sort it as per ecstasy
    results_to_providers["results"].sort(key= lambda x: x["ecstasy"], reverse=True)

    result = json.dumps(results_to_providers)

    resp = Response(result, status=200, mimetype='application/json')

    return resp


if __name__ == '__main__':
    app.run(port=8000) # listening on port 8000

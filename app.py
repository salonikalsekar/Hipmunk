import json

import requests
from flask import Flask, Response, request, jsonify, session, render_template
from scrape_provider_multiprocessing import multiprocess_requests

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

# @app.route('/')
# def index():
#     return render_template("index.html")
#
# @app.route('/hotels/search', methods=["GET"])
# def get_data():
#     """
#     This is the API I've designed that gets the request from 5 endpoints of hotel
#     :return: returns a json response of the search result sorted in descending order based on ecstasy
#     """
#     providers = ['Expedia', 'Orbitz', 'Priceline', 'Travelocity', "Hilton"]
#     results_to_providers = dict()
#
#     try:
#         results_to_providers["results"] = []
#
#         for provider in providers:
#             url = "http://localhost:9000/scrapers/" + provider
#             json_data = json.loads(requests.get(url).content)   # The get request call
#             results_to_providers["results"] += json_data["results"]
#     except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException):
#         not_found()
#
#     # Here I are sorting the result in n * log(n)
#     # Since I didn't get the result in sorted order, I had to explicitly sort it as per ecstasy
#     results_to_providers["results"].sort(key= lambda x: x["ecstasy"], reverse=True)
#     result = json.dumps(results_to_providers)
#
#     resp = Response(result, status=200, mimetype='application/json')
#
#     return results_to_providers


@app.route('/hotels/search', methods=["GET", "POST"])
def get_data():
    """
    This is the API I've designed that gets the request from 5 endpoints of hotel
    :return: returns a json response of the search result sorted in descending order based on ecstasy
    """

    results = multiprocess_requests()
    final = []

    for hd in results:
        for i in hd:
            final.append(i)

    results = {}
    results["results"] = sorted(final, key = lambda x : x['ecstasy'], reverse= True)
    session["hotel_data"] = results["results"]

    resp = json.dumps(results)

    # response = Response(resp, status = 200, mimetype="application/json")
    # return response
    return render_template("index.html", resp = results["results"])

@app.route('/hotels/sort', methods=["GET"])
def sort_data():
    """
    This is the API I've designed that gets the request from 5 endpoints of hotel
    :return: returns a json response of the search result sorted in descending order based on ecstasy
    """

    results = session["hotel_data"]
    print(results)
    # print(results)
    # sorted_res = sorted(results, key = lambda x:x["price"])
    # resp = json.dumps(sorted_res)
    #
    # # response = Response(resp, status = 200, mimetype="application/json")
    # return render_template("index.html", resp = resp)


if __name__ == '__main__':
    app.secret_key = "secret"
    app.run(port=8000) # listening on port 8000

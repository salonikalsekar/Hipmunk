from multiprocessing import Pool as ThreadPool
import requests


def multiprocess_requests():

    providers = ['Expedia', 'Orbitz', 'Travelocity', 'Priceline', 'Hilton']
    thread_pools = ThreadPool(len(providers))
    results = thread_pools.map(scrape_each_provider, providers)

    # since we don't want to do any new pool processing request
    # we close the pools.
    thread_pools.close()

    # We wait for all the worker processes to terminate
    thread_pools.join()

    return results


def scrape_each_provider(provider_name):
    url = 'http://localhost:9000/scrapers/' + provider_name
    return requests.get(url).json()["results"]


# Used for debugging
if __name__ == "__main__":
    print (multiprocess_requests())

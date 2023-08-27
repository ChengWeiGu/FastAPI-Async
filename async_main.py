import requests
import json
import time


def test_get_home():
    ts = time.time()
    # define url
    endpoint = "http://192.168.50.225:8080"
    fun_name = "home"
    url = endpoint + "/" + fun_name
    # define deliver data
    account_id = "David"
    country = "TW"
    json_data = {"account_id":account_id,
                 "country":country}
    json_data = json.dumps(json_data).encode('utf-8')
    resp = requests.get(url,data=json_data)
    if resp.status_code == 200:
        data = resp.json()
        print(data)
    print(f"time: {time.time() - ts} (s)")


def test_get_quota():
    ts = time.time()
    # define url
    endpoint = "http://192.168.50.225:8080"
    fun_name = "get_quota"
    url = endpoint + "/" + fun_name
    # define deliver data
    account_id = "David"
    country = "TW"
    json_data = {"account_id":account_id,
                 "country":country}
    json_data = json.dumps(json_data).encode('utf-8')
    resp = requests.post(url,data=json_data)
    if resp.status_code == 200:
        data = resp.json()
        print(data)
    print(f"time: {time.time() - ts} (s)")


if __name__ == "__main__":
    test_get_home()
    test_get_quota()
import requests


class HTTP:
    def get(self,url,return_to_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_to_json else ''
        return r.json() if return_to_json else r.text

import hmac
import hashlib
from datetime import datetime, timezone

secret = "#######"
api = "#########"
cif = "########"

def get_auth_headers(method, url_path, query_string=""):
    utc_datetime = datetime.now(timezone.utc)
    data_ora = utc_datetime.strftime("%Y-%m-%dT%H:%M:%S") + ".000Z"

    string_to_sign = f"{method}\n{url_path}\n{query_string}\n\n{data_ora}"
    dig = hmac.new(bytes(secret, 'latin-1'), msg=bytes(string_to_sign, 'latin-1'), digestmod=hashlib.sha1).hexdigest()
    firma = f"CWS {api}:{dig.upper()}"

    headers = {
        'Accept': "application/json",
        'DateRequest': data_ora,
        'Authorization': firma
    }
    return headers
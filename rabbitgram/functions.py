import json
import re

def get_shared_data(html):
    match = re.search(r'window._sharedData = ({[^\n]*});', html)
    if not match:
        raise RabbitException("User is not found.")
    return json.loads(match.group(1))

class RabbitException(Exception):
    pass
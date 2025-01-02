import random

import requests

url = ' http://192.168.8.170:9001/predictive/datalog/'

for date in range(20,32):
    for hour in range(24):
        for minute in range(1, 60):
            minute = str(minute)
            if len(minute) == 1:
                minute = '0' + str(minute)

            data = {
                "element_id": "S19",
                "max": random.randint(20, 24),
                "min": random.randint(13, 15),
                "avg": random.randint(16, 21),
                "no_of_records": "60",
                "timestamp": f"2024-12-{date} {hour}:{minute}:19.000",
                "org_id": "19"}

            req = requests.post(url, data)
            if req.status_code == 201:
                print(f"2024-12-{date} {hour}:{minute}:19.000" )
            else:
                print(req.status_code)



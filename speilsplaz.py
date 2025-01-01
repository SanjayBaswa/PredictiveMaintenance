# import random
#
# import requests
#
# url = ' http://192.168.19.119:9001/predictive/datalog/'
#
# for h in range(24):
#     for i in range(1, 60):
#         i = str(i)
#         if len(i) == 1:
#             i = '0' + str(i)
#
#         data = {
#             "element_id": "S19",
#             "max": random.randint(20, 24),
#             "min": random.randint(13, 15),
#             "avg": random.randint(16, 21),
#             "no_of_records": "60",
#             "timestamp": f"2024-12-28 {h}:{i}:19.000",
#             "org_id": "19"}
#
#         req = requests.post(url, data)
#         print(req.json())

a = [
    {
        "element_id": "S19",
        "tag": "NS=4;N=10",
        "org_id": "1",
        "server_ip": "192.168.1.119"
    },
    {
        "element_id": "S1",
        "tag": "NS=4;N=10",
        "org_id": "1",
        "server_ip": "192.168.1.119"
    },
    {
        "element_id": "S2",
        "tag": "NS=4;N=10",
        "org_id": "1",
        "server_ip": "192.168.1.119"
    },
    {
        "element_id": "s3",
        "tag": "NS=4;N=10",
        "org_id": "1",
        "server_ip": "192.168.119.119"
    }
]

dic = {}

for i in a:
    try:dic[i['server_ip']]
    except:dic[i['server_ip']] = {}
    dic[i['server_ip']][i['element_id']] = [i['tag'], i['org_id']]

print(dic)

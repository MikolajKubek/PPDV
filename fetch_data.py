import requests
from datetime import datetime, timedelta
from time import sleep

# start_date = datetime.now()
# while (datetime.now() - start_date) < timedelta(minutes=5):
#     for i in range(1, 7):
#         filename = f"example_data/patient_{i}_date_{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
#         # print(requests.get(f"http://tesla.iem.pw.edu.pl:9080/v2/monitor/{i}").text)
#         with open(filename, "w") as f:
#             f.write(requests.get(f"http://tesla.iem.pw.edu.pl:9080/v2/monitor/{i}").text)
#             print(f"saved {filename}")
#     sleep(2)

import pandas as pd

columns = ["patient_id", "measurement_date", "birthdate", "disabled", "firstname", "id", "lastname", "trace_id", "trace_name",  "L0_value", "L0_anomaly", "L1_value", "L1_anomaly", "L2_value", "L2_anomaly", "R0_value", "R0_anomaly", "R1_value", "R1_anomaly", "R2_value", "R2_anomaly"]

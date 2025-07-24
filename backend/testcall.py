import requests
from datetime import datetime, timedelta



now = datetime.now()
for _ in range(5):
    response = requests.get('http://localhost:8000/api/epg.html?json=1')
    print(len(response.content.decode('utf-8')))
print(datetime.now() - now)
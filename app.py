from flask import Flask, request
from datetime import datetime
import requests
import csv

import os

if not os.path.exists("ip_log.csv"):
    with open("ip_log.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "IP", "Country", "Region", "City", "ZIP", "Lat", "Lon", "ISP", "Google Maps"])




app = Flask(__name__)

def get_geolocation(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    return response.json()

@app.route("/")
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    data = get_geolocation(ip)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if data['status'] == 'success':
        # Log info
        log_entry = {
            'Time': timestamp,
            'IP': ip,
            'Country': data['country'],
            'Region': data['regionName'],
            'City': data['city'],
            'ZIP': data['zip'],
            'Lat': data['lat'],
            'Lon': data['lon'],
            'ISP': data['isp'],
            'Google Maps': f"https://www.google.com/maps/@{data['lat']},{data['lon']},15z"
        }

        with open('ip_log.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=log_entry.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return f"""
        <h2>Welcome — your visit has been logged for cybersecurity testing.</h2>
        <ul>
            <li><strong>IP:</strong> {ip}</li>
            <li><strong>City:</strong> {data['city']}</li>
            <li><strong>Region:</strong> {data['regionName']}</li>
            <li><strong>Country:</strong> {data['country']}</li>
            <li><strong>ZIP:</strong> {data['zip']}</li>
            <li><strong>ISP:</strong> {data['isp']}</li>
            <li><strong>Map:</strong> <a href="https://www.google.com/maps/@{data['lat']},{data['lon']},15z" target="_blank">View</a></li>
        </ul>
        """
    else:
        return """
<!DOCTYPE html>
<html>
<head>
  <title>You Got IP’d 🤪</title>
  <style>
    body { font-family: Arial, text-align: center; background-color: #111; color: #fff; padding-top: 100px; }
    h1 { font-size: 3em; color: #ff4c4c; }
    p { font-size: 1.2em; }
  </style>
</head>
<body>
  <h1>🎯 You Got IP’d 🤪</h1>
  <p>This page was just a test. We hope you had fun.</p>
  <p>Check your WiFi... just kidding 😈</p>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

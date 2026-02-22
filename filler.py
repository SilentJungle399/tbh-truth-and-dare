import requests
import json
import threading

def get_truth():
	response = requests.get("https://api.truthordarebot.xyz/api/truth")
	if response.status_code == 200:
		data = response.json()
		return data["question"]
	else:
		return "Failed to fetch a truth question."
	
def get_dare():
	response = requests.get("https://api.truthordarebot.xyz/api/dare")
	if response.status_code == 200:
		data = response.json()
		return data["question"]
	else:
		return "Failed to fetch a dare."
	
data = {
	"truth": [],
	"dare": []
}

def app(i):
	truth = get_truth()
	dare = get_dare()

	print(f"Truth {i+1}: {truth}")
	print(f"Dare {i+1}: {dare}")

	data["truth"].append(truth)
	data["dare"].append(dare)

for i in range(100):
	thread = threading.Thread(target=app, args=(i,))
	thread.start()

for i in range(100, 130):
	app(i)

with open("data.json", "w") as f:
	json.dump(data, f, indent=4)

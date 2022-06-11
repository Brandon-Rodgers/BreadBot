import requests
import datetime
import calendar

IP = "159.223.168.89"

# Guild Data

def guild_info(guild, timestamp=None):
	if type(guild) == list:
		j = ","
		j.join(guild)

	if timestamp == None:
		timestamp = datetime.datetime.utcnow()

	payload = {'names':guild, 'timestamp':timestamp}
	r = requests.get(f"http://{IP}/api/v1/Guild/Snapshot/Bulk", params=payload)
	data = r.json()
	return data

def guild_members(guild, csv="false"):
	if type(guild) == list:
		j = ","
		j.join(guild)

	payload = {'names':guild, 'csv':csv}
	r = requests.get(f"http://{IP}/api/v1/Guild/Members/Bulk", params=payload)
	if csv == "false":
		data = r.json()
	return data

# User Data

def user_info(name, timestamp=None):
	if type(name) == list:
		j = ","
		j.join(name)

	if timestamp == None:
		timestamp = datetime.datetime.utcnow()

	payload = {'names':name, 'timestamp':timestamp}
	r = requests.get(f"http://{IP}/api/v1/User/Snapshot/Bulk", params=payload)
	data = r.json()
	return data

def user_stones_period(name, start, end=None):
	if type(name) == list:
		j = ","
		j.join(name)

	if end == None:
		end = datetime.datetime.utcnow()

	payload = {'names':name, 'fromDate':start, 'toDate':end}
	r = requests.get(f"http://{IP}/api/v1/User/Aggregate/Period", params=payload)
	data = r.json()
	return data

def user_heroes(name, timestamp=None):
	if timestamp == None:
		timestamp = datetime.datetime.utcnow()

	payload = {'name':name, 'timestamp':timestamp}
	r = requests.get(f"http://{IP}/api/v1/User/Squad", params=payload)
	data = r.json()
	return data

# Leaderboard Data

def user_leaderboard_info(name, option="trophies"): #0 = Trophies, 1 = Total Gold, 2 = Total Stones, 3 = Season XP, 4 = Season Wins, 5 = Season Stones, 6 = Season Chests, 7 = Season Gold
	if type(name) == list:
		j = ","
		j.join(name)

	options = {"trophies":0, "total gold":1, "total stones":2, "season xp":3, "season wins":4, "season stones":5, "season chests":6, "season gold":7}
	payload = {'names':name, 'type':options[option]}
	r = requests.get(f"http://{IP}/api/v1/Leaderboard/User/Bulk", params=payload)
	data = r.json()
	return data

def user_leaderboard_range(pos=0, count=15, option="trophies"): #0 = Trophies, 1 = Total Gold, 2 = Total Stones, 3 = Season XP, 4 = Season Wins, 5 = Season Stones, 6 = Season Chests, 7 = Season Gold
	options = {"trophies":0, "total gold":1, "total stones":2, "season xp":3, "season wins":4, "season stones":5, "season chests":6, "season gold":7}
	payload = {'position':pos, 'count':count, 'type':options[option]}
	r = requests.get(f"http://{IP}/api/v1/Leaderboard/User/Range", params=payload)
	data = r.json()
	return data

def user_leaderboard_page(name, option="trophies"): #0 = Trophies, 1 = Total Gold, 2 = Total Stones, 3 = Season XP, 4 = Season Wins, 5 = Season Stones, 6 = Season Chests, 7 = Season Gold
	options = {"trophies":0, "total gold":1, "total stones":2, "season xp":3, "season wins":4, "season stones":5, "season chests":6, "season gold":7}
	payload = {'name':name, 'type':options[option]}
	r = requests.get(f"http://{IP}/api/v1/Leaderboard/User/Page", params=payload)
	data = r.json()
	return data

def guild_leaderboard_bulk(guild):
	if type(guild) == list:
		j = ","
		j.join(guild)

	payload = {'names':guild}
	r = requests.get(f"http://{IP}/api/v1/Leaderboard/Guild/Bulk", params=payload)
	data = r.json()
	return data

def guild_leaderboard_range(pos=0, count=15):
	payload = {'position':pos, 'count':count}
	r = requests.get(f"http://{IP}/api/v1/Leaderboard/Guild/Range", params=payload)
	data = r.json()
	return data

def guild_leaderboard_page(guild):
	payload = {'name':guild}
	r = requests.get(f"http://{IP}/api/v1/Leaderboard/Guild/Page", params=payload)
	data = r.json()
	return data

# World Event Data

def guild_worldevent_info(guild):
	if type(guild) == list:
		j = ","
		j.join(guild)

	payload = {'names':guild}
	r = requests.get(f"http://{IP}/api/v1/WorldEvent/Guild/Bulk", params=payload)
	data = r.json()
	return data

def guild_worldevent_range(pos=0, count=15):
	payload = {'position':pos, 'count':count}
	r = requests.get(f"http://{IP}/api/v1/WorldEvent/Guild/Range", params=payload)
	data = r.json()
	return data

def guild_worldevent_page(guild):
	payload = {'name':guild}
	r = requests.get(f"http://{IP}/api/v1/WorldEvent/Guild/Page", params=payload)
	data = r.json()
	return data

def user_worldevent_info(name):
	if type(name) == list:
		j = ","
		j.join(name)

	payload = {'names':name}
	r = requests.get(f"http://{IP}/api/v1/WorldEvent/User/Bulk", params=payload)
	data = r.json()
	return data

def user_worldevent_range(pos=0, count=15):
	payload = {'position':pos, 'count':count}
	r = requests.get(f"http://{IP}/api/v1/WorldEvent/User/Range", params=payload)
	data = r.json()
	return data

def user_worldevent_page(name):
	payload = {'name':name}
	r = requests.get(f"http://{IP}/api/v1/WorldEvent/User/Page", params=payload)
	data = r.json()
	return data

if __name__ == "__main__":
	pass
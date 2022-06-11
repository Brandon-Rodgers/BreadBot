def abbreviate_number(number):
    abbreviations = {3:"K", 6:"M", 9:"B", 12:"T", 15:"Qa", 18:"Qi", 21:"Sx"}
    length = len(str(number))
    if length < 4:
        return number, ""

    exp = int(length - ((length-1) % 3)-1)

    return(number/(10**exp),f"{abbreviations[exp]}")

def add_commas_to_number(number):
	number = str(number)
	length = len(number)

	commas = ((length - (length % 3)) // 3)

	if length % 3 == 0:
		commas -= 1

	for i in range(commas):
		split = -3 * (1 * (i+1)) - i
		number = number[:split] + "," + number[split:]

	return number

def seconds_to_hms(time):
	seconds = int(time % 60)
	time = time - seconds
	minutes = int((time % 3600)/60)
	time = time - (minutes * 60)
	hours = int((time % 86400)/3600)
	time = time - (hours * 3600)
	days = int(time /86400)

	return(days, hours, minutes, seconds)

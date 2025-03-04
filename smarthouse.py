import json
from nltk.tokenize import word_tokenize

def changeState(room = "", appl = "", state = "", value = None):
    with open('house.json', 'r') as fp:
        house = json.load(fp)#loads up the current house file

    # if req[0] == "all":
    #     for room in house:
    #         if req[1] in room:
    #             if req[1] == "lights":#change lights
    #                 if req[2] == "on":
    #                     room["lights"]["brightness"] = 100
    #                 elif req[2] == "off":
    #                     room["lights"]["brightness"] = 0
    #             elif type(room[req[1]]) == dict:#things with multiple attributes
    #                 if req[2] == "on":
    #                     room[req[1]]["on"] = True
    #                 elif req[2] == "off":
    #                     room[req[1]]["on"] = False
    #                 else:
    #                     room[req[1]][req[2]] = req[3]
    #             else:#things with just on or off
    #                 if req[2] == "on" or req[2] == "open":
    #                     room[req[1]] = True
    #                 elif req[2] == "off" or req[2] == "close":
    #                     room[req[1]] = False
                
    # for room in house:
    #     # print(room)
    #     if room["room"] == req[0]:#check for room
    #         print("room '" + req[0] + "' exists")
    #         if req[1] in room:#check for thing to change
    #             print("'" + req[1] + "' exists")
    #             if req[1] == "lights":#change lights
    #                 if req[2] == "on":
    #                     room["lights"]["brightness"] = 100
    #                 elif req[2] == "off":
    #                     room["lights"]["brightness"] = 0
    #             elif type(room[req[1]]) == dict:#things with multiple attributes
    #                 if req[2] == "on":
    #                     room[req[1]]["on"] = True
    #                 elif req[2] == "off":
    #                     room[req[1]]["on"] = False
    #                     if req[1] == "oven":
    #                         room["oven"]["temp"] = 0
    #                 else:
    #                     if req[1] == "oven":
    #                         room["oven"]["on"] = True
    #                     room[req[1]][req[2]] = req[3]
    #             else:#things with just on or off
    #                 if req[2] == "on":
    #                     room[req[1]] = True
    #                 elif req[2] == "off":
    #                     room[req[1]] = False

    if room == "all":
        for room in house:
            if appl in house[room]:
                if value:#checks how many
                    if value == "on" or value == "open":#checks for toggle
                        house[room][appl]["on"] = True
                    elif value == "off" or value == "close":
                        house[room][appl]["on"] = False
                    else:
                        house[room][appl][state] = value#if not a toggle sets the state to the value
                        if appl == "oven":
                            house[room]["oven"]["on"] = True

                    print("setting the '" + state + "' of the '" + appl + "' in the '" + room + "' to " + str(value) + "")
                else:
                    if state == "on" or state == "open":#checks for toggle
                        if appl == "lights":#checks for lights
                            house[room][appl]["brightness"] = 100
                        elif appl == "door":
                            house[room][appl]["open"] = True
                        else:
                            house[room][appl]["on"] = True
                    elif state == "off" or state == "close":
                        if appl == "lights":#checks for lights
                            house[room][appl]["brightness"] = 0
                        elif appl == "door":
                            house[room][appl]["open"] = False
                        else:
                            house[room][appl]["on"] = False
                            if appl == "oven":
                                house[room]["oven"]["temp"] = 0
                    else:
                        house[room][appl] = state#if not toggle sets the appliance to the specified state
    else:
        if value:#checks how many
            if value == "on" or value == "open":#checks for toggle
                house[room][appl]["on"] = True
            elif value == "off" or value == "close":
                house[room][appl]["on"] = False
            else:
                house[room][appl][state] = value#if not a toggle sets the state to the value
                if appl == "oven":
                    house[room]["oven"]["on"] = True

            print("setting the '" + state + "' of the '" + appl + "' in the '" + room + "' to " + str(value) + "")
        else:
            if state == "on" or state == "open":#checks for toggle
                if appl == "lights":#checks for lights
                    house[room][appl]["brightness"] = 100
                elif appl == "door":
                    house[room][appl]["open"] = True
                else:
                    house[room][appl]["on"] = True
            elif state == "off" or state == "close":
                if appl == "lights":#checks for lights
                    house[room][appl]["brightness"] = 0
                elif appl == "door":
                    house[room][appl]["open"] = False
                else:
                    house[room][appl]["on"] = False
                    if appl == "oven":
                        house[room]["oven"]["temp"] = 0
            else:
                house[room][appl] = state#if not toggle sets the appliance to the specified state

        print("setting the '" + appl + "' in the '" + room + "' to '" + state + "'")

    with open('house.json', 'w') as fp:
        json.dump(house, fp)#saves the dictionary as a json file

def recallState(room = "", appl = None, state = None):
    with open('house.json', 'r') as fp:
        house = json.load(fp)#loads up the current house file

    if room:
        if appl:
            if state:
                print(room, appl, state)
                return house[room][appl][state]
            else:
                return house[room][appl]
        else:
            return house[room]

def checkInput(term = "", check = False):
    with open('house.json', 'r') as fp:
        house = json.load(fp) # loads up the current house file

    term = term.lower()

    room = ""
    appl = ""
    state = ""
    val = None

    rooms = ["all"]
    appliances = []
    states = ["on", "off", "open", "close", "unlocked", "lock", "unlock"]
    for r in house: # goes through the rooms, their appliances, and their states and adds them to their respective lists
        rooms.append(r)
        for appliance in house[r]:
            appliances.append(appliance)
            if type(house[r][appliance]) == dict:
                for sta in house[r][appliance]:
                    states.append(sta)

    appliances = list(set(appliances))#remove duplicates
    states = list(set(states))

    # print(rooms, appliances, states)

    for r in rooms: # first check for the room
        # if r in term:
        if r in word_tokenize(term):
            room = r
            term = term.replace(r, "")
            break
    # print(room)

    for a in appliances: # check for the appliance
        # print(a, a[-1] == "s" and a[:-1] in term)
        # if a in term or (a[-1] == "s" and a[:-1] in term):
        if a in word_tokenize(term) or (a[-1] == "s" and a[:-1] in word_tokenize(term)):
            appl = a
            term = term.replace(a, "")
            break
    # print(appl)

    if not room: # second check for the room
        if all(appl in house[r] for r in house):# check if it's in all the rooms
            room = "all"
        elif not all(appl in house[r] for r in house) and any(appl in house[r] for r in house): # if it's not in every room, but a few: check which room it's in
            for r in house:
                if appl in house[r]:
                    room = r
                    term = term.replace(r, "")
                    break
    # print(room)

    for s in states: # check for the state
        # if s in term:
        # if s in word_tokenize(term):
        if s in word_tokenize(term) or (s[-1] == "s" and s[:-1] in word_tokenize(term)) or any(s == x[:-1] for x in word_tokenize(term)):
            state = s
            term = term.replace(s, "")
            break
    # print(state)

    # colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    colors = ['alice-blue', 'aqua', 'aquamarine', 'beige', 'black', 'blue', 'blue-violet', 'brown', 'chartreuse', 'chocolate', 'coral', 'crimson', 'cyan', 'dark-blue', 'dark-cyan', 'dark-gray', 'dark-green', 'dark-grey', 'dark-magenta', 'dark-orange', 'dark-red', 'dark-turquoise', 'dark-violet', 'forest-green', 'fuchsia', 'gold', 'gray', 'green', 'green-yellow', 'grey', 'hot-pink', 'indigo', 'lavender', 'light-blue', 'light-cyan', 'light-gray', 'light-green', 'light-grey', 'light-pink', 'light-yellow', 'lime', 'lime-green', 'magenta', 'maroon', 'midnight-blue', 'navy', 'orange', 'orange-red', 'pink', 'plum', 'purple', 'red', 'royal-blue', 'sea-green', 'sky-blue', 'slate-blue', 'slate-gray', 'slate-grey', 'spring-green', 'steel-blue', 'teal', 'turquoise', 'violet', 'white', 'yellow', 'yellow-green']

    # print(term)
    words = word_tokenize(term)
    for i, w in enumerate(words): # check for the value
        if state in ["brightness", "temp", "volume", "input"]:
            if any(x.isdigit() for x in w): # things like 78 and 50 or HDMI1 and VGA2
                if all(x.isdigit() for x in w):
                    val = int(w)
                    break
                else:
                    val = w
                    break
        elif state == "color": # for changing light colors
            if w in colors: # list of color names
                val = w
                break
            elif w == "[" or w == "(": # if it's an rgb/cmyk color value
                current = []
                for x in words[i:]:
                    if x.isdigit():
                        current.append(int(x))
                    elif x == "]" or x == ")":
                        break
                if len(current) == 3 or len(current) == 4:
                    val = current
    # print(val)

    # print(room, appl, state, val)
    # if appl and state:
    if room and appl and state: # if the room, appliance, and state aren't all set, we were unable to get info from the input(whether that means that the input was bad or something is wrong with the extraction methods)
        if check: # specifies if the input is meant to be for checking the state of an appliance or changing it
            return (room, appl, state) # i could try outputing a dictionary instead
        else:
            return (room, appl, state, val)
    else:
        return None

if __name__ == "__main__":
    # s = ("kitchen", "lights", "on", None)
    # s = tuple(input("> ").split(" "))
    # s = eval(input("> "))
    # print(s)
    # changeState(s[0], s[1], s[2], s[3])
    # changeState(input("room: ").lower(), input("appliance: ").lower(), input("state: ").lower(), turn(input("value: ")))
    # room, appli, stat, val = input("room: "), input("appliance: "), input("state: "), input("value: ")

    # # if stat == "":
    # #     stat = None

    # if val:
    #     if val.isnumeric() or val == "None":
    #         val = eval(val)
    # else:
    #     val = None

    # print(checkInput("turn on the lights in the garage"))
    # s = checkInput(input("> "))
    # s = checkInput(input("> "), True)
    # print(s)
    # changeState(room, appli, stat, val)
    # print(recallState(room, appli, stat))
    # print(recallState("kitchen", "lights", None))

    # print(checkInput2("turn on the lights in the garage"))

    t = input("> ")
    s = checkInput(t, False)
    print(s)
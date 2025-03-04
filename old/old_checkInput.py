import json

def checkInput(term = "", check = False):
    with open('house.json', 'r') as fp:
        house = json.load(fp)#loads up the current house file

    room = ""
    appl = ""
    state = ""
    val = None

    # print(house)

    rooms = ["all"]
    appliances = ["light"]
    states = ["on", "off", "open", "close", "unlocked", "lock", "unlock"]
    for r in house:#goes through the rooms, their appliances, and their states and adds them to lists
        rooms.append(r)
        for appliance in house[r]:
            appliances.append(appliance)
            if type(house[r][appliance]) == dict:
                for sta in house[r][appliance]:
                    states.append(sta)

    # rooms = list(set(rooms))
    appliances = list(set(appliances))#remove duplicates
    states = list(set(states))
    # print(rooms, appliances, states) 
    
    term = term.split(" ")#splits the input string into a list by spaces
    for t in term:#goes through every word in the input
        # print(t)
        if t in rooms:
            room = t
        
        if t in appliances:
            appl = t

            if not room:#if room not found yet
                # print(appl, all(True if appl in house[r] else False for r in house))
                if all(appl in house[r] for r in house):#check if the appliance is present in all rooms
                    room = "all"#if the appliance is in every room, set the room to all
                else:#if not, look for the room it is in
                    for r in house:
                        if appl in house[r]:
                            room = r
                # print(room)

        # print(bool(state), state)
        if appl and not state:
            if t != appl:
                if t in states:
                    state = t
                elif t.isdigit():
                    # print("toot")
                    state = eval(t) # BAD
                    if appl == "oven":
                        state = "temp"
                        val = eval(t) # BAD

    if not val:
        start = 0
        end = 0
        for i, j in enumerate(term):
            if "[" in j:
                start = i
            elif "]" in j:
                end = i + 1

        if start != end:
            # print(term[start:end])
            val = eval(" ".join(term[start:end])) # BAD
            if appl == "lights":
                state = "color"
        elif any(v.isdigit() for v in term):
            # print(state, term[-1])
            [val := eval(v) for v in term if v.isdigit() and v != str(state)] # BAD
        else:
            if term[-1] != room and term[-2] != room and term[-1] != state and term[-1] != appl:
                val = term[-1]

    if appl == "light":#makes sure it matches the actual name
        appl = "lights"

    # print(room, appl, state, val)
    if room != "all":
        if type(house[room][appl]) == dict:
            if state not in house[room][appl] or state not in ["on", "off", "open", "close"]:
                for x in term:
                    if x in house[room][appl] or x == "on" or x == "off" or x == "open" or x == "close":
                        state = x
    else:
        # print(room, appl, state, val)
        for r in house:
            if appl in house[r]:
                if type(house[r][appl]) == dict:
                    if state not in house[r][appl]:
                        for x in term:
                            if x in house[r][appl] or x == "on" or x == "off" or x == "open" or x == "close":
                                state = x
                else:
                    state = int(val)
        val = None

    if check:
        return (room, appl, state)
    else:
        return (room, appl, state, val)

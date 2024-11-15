import PySimpleGUI as sg
import random

use_custom_titlebar= True if sg.running_trinket() else False
red = "#AA4A44"
green = "#c2ffa7"

def makeRoles(num):
    roleList = []
    for i in range(0,num):
        if i == 0:
            roleList.append("D") 
        elif i == 1:
            roleList.append("SB")
        elif i == 2:
            roleList.append("BB")
        elif i == 3:
            roleList.append("UTG")
        elif i == num-1: 
            roleList.append("C")
        elif i == num-2:
            roleList.append("HJ")
        elif i == num-3:
            roleList.append("LJ")
        else:
            roleList.append("UTG + " +  str(i-3))                                          
    return roleList

def create_players(sb,bb,namelist):
    num = len(namelist)
    players = []
    rolelist = makeRoles(num)
    for i in range(1,num+1):
        bet = 0
        if i == 2:
            bet = sb
        if i == 3:
            bet = bb
        players.append([i, random.randint(1,99999), rolelist[i-1], bet, namelist[i-1]])

    return players

#print(str(create_players(5,1,2)))

def create_layouts(players):
    layouts = []
    for player in players:
        name = player[0]
        card = player[1]
        position = player[2]
        bet = player[3]
        playername =  player[4]
        if player[2] == "UTG":
            color = green
        else:
            color = red
        layout = [
                [sg.Frame(str("Player " + str(name)), [[sg.StatusBar("Action", text_color=color, key="-SP" + str(name) + "-")], [sg.Text(playername)], [sg.Text(str(card))], [sg.Multiline(position, s=8, disabled=True, no_scrollbar=True, key=('-PP'+ str(name) + '-'))], [sg.Text(str(bet), key=('-BP' + str(name) + '-'))]])]
    ]
        layouts.append(layout)

    return layouts

#print(str(create_layouts(create_players(3,100,200))))

def make_window(players):

    Menu = sg.Menu   

    layouts = create_layouts(players)   

    layout_action = [
                [sg.Frame("Action", [[sg.Button("Check")], [sg.Button("Fold")], [sg.Button("Bet"), sg.Input(s=5, key = "-BET-")], [sg.Button("Call")], [sg.Button("Raise"), sg.Input(s=5, key = '-RAISE-')], [sg.Button("All In")]])]
    ]

    layout_hand = [
                [sg.Frame("Hand", [[sg.Button("Next Hand")]])]
    ]
    
    layout_street = [
                [sg.Frame("Street", [[sg.StatusBar("Pre-flop", text_color=green, key = '-S1-')], [sg.StatusBar("Flop", text_color=red, key = '-S2-')], [sg.StatusBar("Turn", text_color=red, key="-S3-")], [sg.StatusBar("River", text_color=red, key = "-S4-")]])]
    ]
    

    player_layout = []
    for l in layouts:
        player_layout.append(sg.Col(l, p=0))

    layout = [[Menu([['File', ['Exit']], ['Edit', ['Edit Me', ]]],  k='-CUST MENUBAR-',p=0)],
              [sg.T('RFID Poker Table Backend GUI', font='_ 14', justification='c', expand_x=True)],
              player_layout,
              [sg.Col(layout_action, p=0), sg.Col(layout_street, p=0)],
              [sg.Col(layout_hand, p=0)]]
    
    
    window = sg.Window('Poker', layout, finalize=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True, use_custom_titlebar=use_custom_titlebar)

    return window

sb = 100
bb = 200
names = ["Warren", "Tully", "Johnny", "Ben", "Gilbert", "Cooper"]
players = create_players(sb,bb,names)
window = make_window(players)
action = 4
dealer = 0
betsize = bb
foldedplayers = []
actioncount = 0
playercount = len(names)
street = 1

def move_position(action):
    num = len(names)
    for i in range(1,num+1):
        window["-BP" + str(i) + '-'].update(0)

    rolelist = makeRoles(num)
    for i in range(1,num+1):
        key = '-PP' + str(i) + '-'
        role = str(values[key])
        if role == "D":
            window["-SP" + str(action) + '-'].update(text_color="#AA4A44")
            window["-SP" + str((i+3)%num + 1) + '-'].update(text_color="#c2ffa7")
            action = (i+3)%num + 1
            window["-BP" + str((i+1)%num + 1) + '-'].update(sb)
            window["-BP" + str((i+2)%num + 1) + '-'].update(bb)
        for j in range(num):
            if role == rolelist[j]:
                role = rolelist[(j-1)%num]
                break
        window[key].update(role)
    return(action)

def move_action(action):
    key = '-SP' + str(action) + '-'
    window[key].update(text_color="#AA4A44")
    action = action%len(names) + 1
    key = '-SP' + str(action) + '-'
    window[key].update(text_color="#c2ffa7")

    for player in foldedplayers:
        if action == player:
            action = move_action(action)

    return action

def check_action(action):
    key = '-BP' + str(action) + '-'
    #if values[]

def move_street(street): 
    key = '-S' + str(street) + '-'
    window[key].update(text_color=red)
    if street == 4:
        return 4
    street = street%4 + 1
    key = "-S" + str(street) + '-'
    window[key].update(text_color=green)



    return street


while True:
    event, values = window.read()
    # sg.Print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Edit Me':
        sg.execute_editor(__file__) 
    if event == "Check":
        action = move_action(action)
        actioncount += 1
    if event == "Bet":
        bet = values["-BET-"]
        betsize = bet
        key = '-BP' + str(action) + '-' 
        window[key].update(bet)
        window["-BET-"].update("")
        action = move_action(action)
        actioncount = 1
    if event == "Fold":
        key = '-BP' + str(action) + '-' 
        window[key].update("X")
        foldedplayers.append(action)
        action = move_action(action)
        playercount -= 1
    if event == "Call":
        key = '-BP' + str(action) + '-'
        window[key].update(betsize)
        action = move_action(action)
        actioncount += 1
    if event == "Raise":
        bet = values["-RAISE-"]
        betsize = bet
        key = '-BP' + str(action) + '-' 
        window[key].update(bet)
        window["-RAISE-"].update("")
        action = move_action(action)
        actioncount = 1
    if event == "Next Hand":
        action = move_position(action)
        playercount = len(names)
        foldedplayers = []
        window["-S1-"].update(text_color=green)

    if actioncount == playercount:
        street = move_street(street)
        actioncount = 0
        for i in range(1,len(names) + 1):
            update = True
            key = '-BP' + str(i) + '-'
            for j in foldedplayers:
                if i == j:
                    update = False
            if update:
                window[key].update(0)
        for i in range(1,len(names) + 1):
            key = '-PP' + str(i) + '-'
            if values[key] == "SB":
                window["-SP" + str(i) + '-'].update(text_color=green)
                action = i
            else:
                window["-SP" + str(i) + '-'].update(text_color=red)
    for p in foldedplayers:
        if action == p:
            action = move_action(action)            


window.close()
print(actioncount)
print(playercount)

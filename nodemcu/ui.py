import tkinter as tk
from tkinter import ttk
import subprocess
import json

def getoptions():
    with open('./astardistancesdata.json','r') as file:
        data=json.load(file)
    counter=0
    for item in data:
        for key,value in item.items():
            if str(key).startswith('k') or str(key).startswith('K'):
                counter=counter+1
    tables=[]
    for i in range(counter):
        tables.append(str(i+1))
    return tables

def run_python_file():
    subprocess.run(["python", "./main.py"])

# Function to find an item by key
def find_item_by_key(data, search_key):
    for item in data:
        if search_key in item:
            return item
    return None

def determine_direction(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    if x1 == x2:
        if y2 < y1:
            return "Up"
        else:
            return "Down"
    elif y1 == y2:
        if x2 > x1:
            return "Right"
        else:
            return "Left"
    return "Unknown"  # Default case if no other conditions are met

def determine_directions(points):
    directions = []

    if len(points) < 2:
        return directions  # Not enough points to determine direction

    # Determine initial direction
    initial_direction = determine_direction(points[0], points[1])
    directions.append(initial_direction)
    
    previous_direction = initial_direction

    for i in range(1, len(points) - 1):
        current_point = points[i]
        next_point = points[i + 1]
        
        current_direction = determine_direction(current_point, next_point)

        if current_direction == previous_direction:
            directions.append("Continue")
        else:
            directions.append(current_direction)
            previous_direction = current_direction

    return directions

import socket

# ESP-WROOM-32 IP address and port
host = '192.168.76.6'  # Replace with the actual IP address of your ESP-WROOM-32
port = 80


# def send_data(data):
#     try:
#         # Create a socket object

#         # Connect to the ESP-WROOM-32 server

#         # Send data to the server

#         # Receive response from the server
        


#         # Close the connection
#         # return response
#     except Exception as e:
#         print(f"Failed to send/receive data: {e}")

def sendroutestocontroller(x):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(x)
    startdirection=x[0]
    x.pop(0)
    print(x)
    while x:
        currentcommand=''
        # print(x[0])
        if x[0] == "Continue":
            currentcommand= 'w'
        elif x[0]== "Up" and startdirection=="Left":
            currentcommand= 'd'
        elif x[0]== "Up" and startdirection=="Right":
            currentcommand= 'a'

        elif x[0]== "Left" and startdirection=="Up":
            currentcommand= 'a'
        elif x[0]== "Left" and startdirection=="Down":
            currentcommand= 'd'

        elif x[0]== "Right" and startdirection=="Up":
            currentcommand= 'd'
        elif x[0]== "Right" and startdirection=="Down":
            currentcommand= 'a'
        
        elif x[0]== "Down" and startdirection=="Right":
            currentcommand= 'd'
        elif x[0]== "Down" and startdirection=="Left":
            currentcommand= 'a'
        
        if x[0] != "Continue":
            startdirection=x[0]
        x.pop(0)

        print("yaraab",currentcommand)


        while True:
            print("plz", currentcommand.encode())
            client_socket.sendall(currentcommand.encode() + b'\n')

            # # Receive response from the server
            response = client_socket.recv(1024)
            print("Response from ESP-WROOM-32:", response.decode())
            if response.decode()=="Done":
                break
    client_socket.close()
            
    # while True:
    #     prev=x[0]
    #     x.pop(0)
    #     while x:
    #         # print(x[])
    #         # status = False
    #         response="notdone"
    #         while response!="Done":
    #             data=''
    #             if x[0]=="Continue":
    #                 data='d'
    #                 # continue
    #             elif x[0]=="Left" and prev =="Up":
    #                 data='a'
    #             elif x[0]=="Right" and prev =="Up":
    #                 data='d'


    #             elif x[0]=="Up" and prev =="Right":
    #                 data='a'
    #             elif x[0]=="Down" and prev =="Right":
    #                 data='d'


    #             elif x[0]=="Left" and prev =="Down":
    #                 data='a'
    #             elif x[0]=="Right" and prev =="Down":
    #                 data='d'


    #             elif x[0]=="Down" and prev =="Left":
    #                 data='a'
    #             elif x[0]=="Up" and prev =="Left":
    #                 data='d'
                
    #             client_socket.sendall(data.encode() + b'\n')
    #             response = client_socket.recv(1024)
    #             print("Response from ESP-WROOM-32:", response.decode())

            
    #             if x[0]!="Continue":
    #                 prev=x[0]
    #             print("response is:  ",response)
            
    #         print('pooppedd')
    #         x.pop(0)
    #     client_socket.close()
    #     return

        # response = send_data('s')

    






















def sendroute():
    value1 = combo1.get()
    value2 = combo2.get()


    with open('./astardistancesdata.json', 'r') as file:
        data = json.load(file)

    search_key1 = 'k'+value1
    result1 = find_item_by_key(data, search_key1)

    if value2 !="None":
        search_key2 = 'k'+value2
        result2 = find_item_by_key(data, search_key2)
        if result1.get('cost') < result2.get('cost'):
            sendroutestocontroller(result1.get(search_key1))
        else:
            sendroutestocontroller(result1.get(search_key1))

    else:
        route=result1.get(search_key1)
        goroute= determine_directions(route)
        sendroutestocontroller(goroute)
        # returnresult1=find_item_by_key(data,value1+'k')

        # returnroute=determine_directions(returnresult1.get(value1+'k'))
        # sendroutestocontroller(returnroute)



    # print(result1.get('cost'))
    # print(result1.get(search_key1))
    # print(result2.get('cost'))
    # print(result2.get(search_key2))




    print(f"Combo Box 1: {value1}, Combo Box 2: {value2}")

def update_options(event):
    selected_option = combo1.get()
    remaining_options = [option for option in options if option != selected_option]
    remaining_options.append("None")
    combo2['values'] = remaining_options
    if combo2.get() not in remaining_options:
        combo2.set('None')

# Initial options for combo boxes
options = getoptions()

# Create the main window
root = tk.Tk()
root.title("Robotic Waiter")
root.geometry("400x250")

# Configure the root grid
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a frame for better layout management
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add a title label
title_label = ttk.Label(frame, text="Welcome to Our Restuarant", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Add a button to run a specific Python file
run_button = ttk.Button(frame, text="Edit Restaurant Layout", command=run_python_file)
run_button.grid(row=1, column=0, columnspan=2, pady=10, ipadx=10)

# Add the first combo box
ttk.Label(frame, text="First Table", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
combo1 = ttk.Combobox(frame, values=options, font=("Helvetica", 12), state="readonly")
combo1.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
combo1.current(0)  # Set default value
combo1.bind("<<ComboboxSelected>>", update_options)

# Add the second combo box with an extra "None" option
ttk.Label(frame, text="Second Table:", font=("Helvetica", 12)).grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
combo2 = ttk.Combobox(frame, values=options + ["None"], font=("Helvetica", 12), state="readonly")
combo2.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
combo2.set("None")  # Set default value to "None"

# Add a button to print combo box values
print_button = ttk.Button(frame, text="Go", command=sendroute)
print_button.grid(row=4, column=0, columnspan=2, pady=20, ipadx=10)

# Start the GUI event loop
root.mainloop()

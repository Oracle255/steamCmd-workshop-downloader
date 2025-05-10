import re
import os
import subprocess
#from flask import Flask, request, render_template_string

# TODO : buat interface web dengan flask

steamCmdPath = ""

def convertDownloadCommand():
    global steamCmdPath
    workshop_id = ""
    download_command = "workshop_download_item"
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path_input = os.path.join(directory, "steam_list.txt")
    file_path_output = os.path.join(directory, "output_download_list.txt")
    
    if not os.path.exists(file_path_input):
        with open(file_path_input, "w") as f:
            print("missing input file, creating one....")
            f.write("steamCmdPath=\nWorkshop_id=\n\n#PASTE steamworkshop id below")
            
    if not os.path.exists(file_path_output):
        with open(file_path_output, "w") as f:
            print("missing input file, creating one....")
            f.write("#empty. please run the first option first")        
    
    with open(file_path_input, "r") as file_inp, open(file_path_output, "w") as file_out:
        for line in file_inp:
            # cek lokasi steamCMD
            steamCmd_match = re.search(r'steamCmdPath=(.+)', line)
            if steamCmd_match:
                steamCmdPath = steamCmd_match.group(1).strip()
                continue

            # cek Workshop_id
            workshop_match = re.search(r'Workshop_id=(\d+)', line)
            if workshop_match:
                workshop_id = workshop_match.group(1).strip()
                continue

            # cek mod ID
            item_match = re.search(r'\?id=(\d+)', line)
            if not item_match:
                continue

            # bangun command sequence bwt steamcmd
            final_output = f"{download_command} {workshop_id} {item_match.group(1)}"
            file_out.write("login anonymous\n")
            file_out.write(final_output + "\n")
            file_out.write("\nquit")
            print(final_output)

def runSteamCmd():
    global steamCmdPath
    if not steamCmdPath:
        print("Error: steamCmdPath is empty. Run option 1 first.")
        return

    if not os.path.exists(steamCmdPath):
        print(f"Error: steamCmdPath not found: {steamCmdPath}")
        return

    try:
        subprocess.run([steamCmdPath, "+runscript", "output_download_list.txt"])
    except Exception as e:
        print(f"Error while running steamcmd: {e}")

def main():
    while True:
        print("\nFile Parser Menu:")
        print("1. convert list to steamcmd command")
        print("2. run steamcmd")
        print("3. Exit")
        choice = input("Choose an option (1-9): ")
        if choice == "1":
            convertDownloadCommand()
        elif choice == "2":
            runSteamCmd()
        elif choice == "3":
            break
        else:
            print("invalid option")

main()

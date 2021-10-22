#! /usr/bin/python3
#VAUGHN WOERPEL (vww9966) NSSA 221, 10/22/2021

import csv
import sys
from os import system, name
import subprocess
import os
import time

#Method to clear the display to easily make a nice UI
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

#Method to initially create the shortcut
def create_shortcut():
	clear() #Clears for readability
	fname = input("Please enter the file you would like to make a shortcut for:\t") #Takes in user input of file

	#Checks to see if the file exists, if not, reruns the create shortcut
	if not os.path.exists(fname):		
		choice = input("File does not exist.\nPress 'Enter' to return to try again, or 'Q/q' to quit.")
		if choice=="Q" or choice=="q" or choice=='quit':
			menu()
		create_shortcut()
	#Gets the path for the home directory as well as the path of the file itself, then displays it
	path = os.path.abspath(fname)
	home = os.path.expanduser("~") + "/" + fname
	print("\nFile found:\t" + path)
	#Allows the user to determine if they want to create the link
	selection = input("Create a shortcut for this file? (Y/y):\t")
	if selection == 'y' or selection == 'Y':
		#Handles the link existing
		try:
			os.symlink(path, home) #Creates the link
			print("Symbolic link to home directory created.")
		except:
			print("File already exists.")
	#Allows user to return to main menu
	input("Press 'Enter' to return to the main menu.")
	menu()

#Method to remove the shortcut
def remove_shortcut():
	clear() #Clears for readability
	fname = input("Please enter the file you would like to unlink:\t") #Takes in user input of file
	#Gets the path then sees if the file exists. If it does not, reruns this method
	path = os.path.expanduser("~") + "/" + fname
	if not os.path.exists(path):		
		choice = input("File does not exist.\nPress 'Enter' to return to try again, or 'Q/q' to quit.")
		if choice=="Q" or choice=="q" or choice=='quit':
			menu()
		remove_shortcut()
	#Allows the user to choose to remove it
	selection = input("Remove the link for this file? (Y/y):\t")
	if selection == 'y' or selection == 'Y':
		#Handles if the file doesnt exist
		try:
			os.unlink(path)
			print("Succesfully unlinked.")
		except:
			print("File does not exist.")
	#Allows the user to return to main menu
	input("Press 'Enter' to return to the main menu.")
	menu()

#Method to generate the report
def report():
	clear() #Clears and shows a nice header for readability
	print("\t\t****************************************")
	print("\t\t************ Shorcut Report ************")
	print("\t\t****************************************")
	print()
	#Prints cwd
	print("Your current working directory is " + os.path.expanduser("~"))
	count = 0
	#Runs ls on the path of the users home dir, and then splits it into individual file names
	files_in_dir = subprocess.check_output(['ls',os.path.expanduser("~")]).decode("utf-8").split("\n")
	#For each file, checks to see if it is a symbolic link to another file. If so, increments count
	for file in files_in_dir:
		if(os.path.islink(os.path.expanduser("~") + "/" + file)):
			count = count + 1
	#Displays number of symbolic links
	print("\nNumber of links is " + str(count))
	#Prints all of the links and where they lead to
	print("\nSymbolic Links\t\tTarget Path")
	for file in files_in_dir:
		if(os.path.islink(os.path.expanduser("~") + "/" + file)):
			#Runs readlink to see where the link points to
			print(file + "\t\t" + subprocess.check_output(["readlink","-f",file]).decode("utf-8"))
	#Allows user to return to menu
	input("Press 'Enter' to return to the main menu.")
	menu()



def menu():
	clear() #Clears and shows header for readability
	print("\t\t****************************************")
	print("\t\t*********** Shorcut Creater ************")
	print("\t\t****************************************")
	print()

	#Takes user input for what selection to follow
	choice = input("""
    Enter Selection:
        1 - Create a shortcut in your home directory.
        2 - Remove a shortcut from your home directory.
        3 - Run a shortcut report

    Please enter a number (1-3) or "Q/q" to quit the program. """)

	#Goes to each selection
	if choice == "1":
		create_shortcut()
	elif choice == "2":
		remove_shortcut()
	elif choice == "3":
		report()
	#Allows for user to quit
	elif choice=="Q" or choice=="q" or choice=='quit':
		sys.exit
	else:
		print("\n\tYou have entered an invalid option.")
		time.sleep(3)
		#print("\n\n Please select a number between 1 through 3.")
		menu()
    
#the program is initiated, so to speak, here
menu()
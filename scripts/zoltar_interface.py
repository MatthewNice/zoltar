#!/usr/bin/env python3

# print("Drop 25 cents here..")
#
# wish = input("--Zoltar says: MAKE YOUR WISH--")
#
#
# print("Press Red Button to make your wish.")
#
# #confirm
#
# print("ZOLTAR SPEAKS")
#
# print("Your Wish is Granted")


import sys
n = len(sys.argv)

# parse the input arguments
import argparse
myParser = argparse.ArgumentParser(description="Translates command line inputs from Zoltar script into actionable commands.")
myParser.add_argument('--wish', '-w', help="(wish) the text requesting a speed change", type=str)
# parser.add_argument('--input', '-i', help="Default speeds (csv)", type=str)


args=myParser.parse_args()
wishText = args.wish
# inputFile = args.input

if( None in [wishText] ):
    print(myParser.format_help())
    exit()


from quantulum3 import parser

quantity = parser.parse(wishText)

outputText = []

##units stuff
if quantity.unit.name == 'dimensionless':
    outputText.append("I will assume your units are mph.\n")
else:
    outputText.append("I see your units are ",quantity.unit.name,'\n')

##TODO  check to see if zoltar is allowed, stored in a file

##############################

outputText.append("I will change the vehicles desired speed to your request: ", quantity.value, quantity.unit.name,'\n')

###TODO output value to bash script, where the change is handled

for t in outputText:
    print(t)

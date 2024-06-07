#!/bin/bash

###CHECK TO SEE IF ZOLTAR MODE IS ENGAGED
z_a_val=$(rostopic echo -n 1 /zoltar_allowed)
z_array=($z_a_val)
ZOLTAR_ALLOWED=${z_array[1]}
###
###IF NO
if [[ "$ZOLTAR_ALLOWED" = False ]]; then
  echo "Zoltar mode is not allowed. Return after engaging Sport mode and flashing the high beams twice."

###IF YES
else
  currentZoltar=$(cat ../zoltar_speed.txt)
  echo "The current Zoltar Speed in m/s is: "
  echo $currentZoltar
  echo -n "Enter a speed in MPH. What is your wish?"
  read -r wish

  ##make the output of this script be read into a variable
  # settingRequest=$(python3 zoltar_interface.py -w $wish 2<&1)

  ##use the request variable to change the zoltar_speed.txt
  ###
  if ! [[ $yournumber =~ $re ]] ; then
   echo "error: Not a number" >&2; exit 1
  else
    var=$(awk -v wish=$wish 'BEGIN { print wish*0.44704 }')
    echo $var > ../zoltar_speed.txt
    rostopic pub -1 /zoltar_request std_msgs/Float64 $var
  fi
  ###

  echo
  echo "This was your request:"
  echo "$wish"
  echo
  echo  "YOUR WISH IS GRANTED"

fi

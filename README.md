#Zoltar App

This libpanda application is a mode of operation for experimental vehicle automation. 

##Activation State

The desired speed of the vehicle will follow the speed set by the driver using the familiar cruise control paradigm by default.
To enter into 'Zoltar Mode' the driver will turn the car to 'Sport' and flash the high beam lights twice. At this time, the vehicle will enter 'Zoltar Mode'.

##De-Activation

The driver can return to cruise control by turning 'Sport' off, or return to manual control by pressing 'cancel' or the brake pedal.


##Usage

While active, a passenger can write to 'Zoltar' via CLI and 'wish' for the car to change its desired speed. These are the only kinds of wishes grant-able in alpha version. If possible, Zoltar will
return your message with 'Your Wish is Granted' and the set speed of the car will change.

''zoltar "change the car's velocity setting to 72 mph"''


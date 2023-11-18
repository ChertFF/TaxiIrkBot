from time import strftime, gmtime

time = "23:00"
time = int(time[:2])
print(time)
if time <=2:
    time = time+24
    print (time)

if time - 8 - int(strftime("%H", gmtime())) <= 2:
    print (False)
else:
    print (True)
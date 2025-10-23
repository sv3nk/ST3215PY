from ST3215PY import ST3215PY
import time

# Computer-specific information.
# In this example, waveshare board is connected to port COM4
# Change this depending on your port
DEVICENAME = 'COM4'

servoControl = ST3215PY(DEVICENAME)

# Provides a list of servos and their IDs
# IMPORTANT: If you did not change the ID yet, all servos will have the ID 1
# You will have to change all but one to a different ID
servoList = servoControl.ListServos()
print('Your servos are:')
print(servoList)

time.sleep(2)

# In order to change a servos ID, you must do the following
# 1. Unlock EPROM of the servo
# servoControl.UnlockEprom(1)

# 2. Set new ID
# In this case, change the ID of the servo with ID 1 to ID 3
# servoControl.SetServoId(1, 3)

# 3. Lock the EPROM of the servo (now ID 3)
# servoControl.LockEprom(3)

# Ping a single servo (ID 1 in this case) to see if communication is possible
servoControl.PingServo(1)

time.sleep(2)

# Query a servo and read its position and speed
position, speed = servoControl.ReadPositionSpeed(1)
print('Position: ' + str(position))
print('Speed: ' + str(speed))

time.sleep(2)

# Tell a servo to go to a certain position by specifying:
# Servo ID, Position, Speed, Acceleration
setServoPosition = servoControl.WritePosition(1, 2513, 2400, 50)
if setServoPosition == True:
    print('Position of servo changed')

time.sleep(2)

# SyncRead and SyncWrite are synchronous actions
# Synchronous actions execute read and writes on all specified servos at the same time
# It saves time, is faster and results in less overhead

# Read data of servo 1 and 2 at the same time
readSync = servoControl.SyncRead([1,2])
print('Sync Reading Output:')
print(readSync)

time.sleep(2)

# WriteSync requires the data to be in a certain structure
# Each servo is represented by an array [id, position, speed, acceleration]

servo1 = [1, 4090, 3400, 50]
servo2 = [2, 0, 3400, 50]

# The SyncWrite function takes in an array of arrays and executes the order at the same time on all servos
writeSync = servoControl.SyncWrite([servo1, servo2])
if writeSync == True:
    print('Sync Writing to servos successful')

time.sleep(2)

print('New positions of servos:')
print(servoControl.SyncRead([1,2]))



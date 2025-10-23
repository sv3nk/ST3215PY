from .constants import *
from .protocol_packet_handler import *
from .port_handler import *
from .group_sync_write import *
from .group_sync_read import *


class ST3215PY(protocol_packet_handler):

    def __init__(self, device):
        print("ST3215PY Class initiated")

        self.portHandler = PortHandler(device)

        if not self.portHandler.openPort():
            raise ValueError(f"Could not open port: {device}")

        protocol_packet_handler.__init__(self, self.portHandler)
        
        self.groupSyncRead = GroupSyncRead(self, STS_PRESENT_POSITION_L, 11)
        self.groupSyncWrite = GroupSyncWrite(self, STS_ACC, 7)

    def PingServo(self, sts_id):
        """
        Check the presence of a servo.

        :param sts_id: Servo ID

        :return: True in case of success otherwise False
        """
        modelNum, commResult, error = self.ping(sts_id)
        if commResult == COMM_SUCCESS:
            print('Servo with ID ' + str(sts_id) + ' and model number ' + str(modelNum) + ' pinged successfully.')
            return True
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            
            return False

    def ListServos(self):
        """
        Scan the bus to determine all servo present

        :return: A list of servo ID
        """
        servos = []
        for id in range(0, 4):
            if self.PingServo(id):
                servos.append(id)

        return servos

    def ReadVoltage(self, sts_id):
        """
        Current Voltage of the servo.

        :param sts_id: Servo ID

        :return: Current Voltage in V. None in case of error.
        """
        voltage, commResult, error = self.read1ByteTxRx(sts_id, STS_PRESENT_VOLTAGE)
        if commResult == COMM_SUCCESS and error == 0:
            return voltage * 0.1
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            return None

    def ReadCurrent(self, sts_id):
        """
        Current current of the servo.

        :param sts_id: Servo ID

        :return: Current current in mA. None in case of error.
        """
        current, commResult, error = self.read1ByteTxRx(sts_id, STS_PRESENT_CURRENT_L)
        if commResult == COMM_SUCCESS and error == 0:
            return current * 6.5
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            return None

    def ReadTemperature(self, sts_id):
        """
        Current temperature of the servo.

        :param sts_id: Servo ID

        :return: Current temperature in °C. None in case of error.
        """
        temperature, commResult, error = self.read1ByteTxRx(sts_id, STS_PRESENT_TEMPERATURE)
        if commResult == COMM_SUCCESS and error == 0:
            return temperature
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            return None

    def ReadAccelaration(self, sts_id):
        """
        Current value of the acceleration of the servo.

        :param sts_id: Servo ID

        :return: Current acceleration value. None in case of error.
        """
        acc, commResult, error = self.read1ByteTxRx(sts_id, STS_ACC)
        if commResult == COMM_SUCCESS and error == 0:
            return acc
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            return None
    
    def ReadPosition(self, sts_id):
        """
        Get the current position

        :param sts_id: Servo ID

        :return: position in case of success, otherwise None
        """
        position, commResult, error = self.read2ByteTxRx(sts_id, STS_PRESENT_POSITION_L)
        if commResult == COMM_SUCCESS and error == 0:
            return self.sts_tohost(position, 15)
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            return None
    
    def ReadSpeed(self, sts_id):
        """
        Get the current speed

        :param sts_id: Servo ID

        :return: speed in case of success, otherwise None
        """
        speed, commResult, error = self.read2ByteTxRx(sts_id, STS_PRESENT_SPEED_L)
        if commResult == COMM_SUCCESS and error == 0:
            return self.sts_tohost(speed, 15)
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            return None
    
    def ReadPositionSpeed(self, sts_id):
        """
        Get the current position and speed

        :param sts_id: Servo ID

        :return: position and speed in case of success, otherwise None
        """
        positionSpeed, commResult, error = self.read4ByteTxRx(sts_id, STS_PRESENT_POSITION_L)
        if commResult == COMM_SUCCESS and error == 0:
            position = self.sts_loword(positionSpeed)
            speed = self.sts_hiword(positionSpeed)
            return self.sts_tohost(position, 15), self.sts_tohost(speed, 15)
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            return None
    
    def ReadMoving(self, sts_id):
        """
        Get the current moving status

        :param sts_id: Servo ID

        :return: In case of success, if servo is moving returns True, otherwise False. None in case of error.
        """
        moving, commResult, error = self.read1ByteTxRx(sts_id, STS_MOVING)
        if commResult == COMM_SUCCESS and error == 0:
            return moving
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            if(error != 0):
                print('Error:')
                print(self.getRxPacketError(error))
            return None
    
    def UnlockEprom(self, sts_id):
        """
        Unlock the servo Eprom.

        :param sts_id: Servo ID

        :return: True in case of success, False otherwise
        """
        commResult = self.write1ByteTxRx(sts_id, STS_LOCK, 0)
        if commResult == COMM_SUCCESS:
            return True
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            print('Error unlocking Eprom')
            return False
    
    def LockEprom(self, sts_id):
        """
        Lock the servo Eprom.

        :param sts_id: Servo ID

        :return: True in case of success, False otherwise
        """
        commResult = self.write1ByteTxRx(sts_id, STS_LOCK, 1)
        if commResult == COMM_SUCCESS:
            return True
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            print('Error locking Eprom')
            return False
    
    def SetServoId(self, sts_id, new_sts_id):
        """
        Change ID of a Servo.

        :param sts_id: Actual ID for the servo (1 for a brand new servo)
        :param new_id: New ID for the servo

        :return: None when sucedeed otherwise the error message
        """
        commResult = self.write1ByteTxRx(sts_id, STS_ID, new_sts_id)
        if commResult == COMM_SUCCESS:
            return True
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            return False
    
    def WritePosition(self, sts_id, position, speed, acc):
        """
        Move Servo to a specific position.

        :param sts_id: ID of the servo
        :param position: Target position, between 0 and 4096
        :param speed: Speed at which to move the servo, max is 3400
        :param acc: Acceleration of the servo, max is 256

        :return: Return true if successful, False otherwise
        """
        txpacket = [acc, self.sts_lobyte(position), self.sts_hibyte(position), 0, 0, self.sts_lobyte(speed), self.sts_hibyte(speed)]
        commResult, error = self.writeTxRx(sts_id, STS_ACC, len(txpacket), txpacket)
        if commResult == COMM_SUCCESS and error == 0:
            return True
        else:
            print('CommResult:')
            print(self.getTxRxResult(commResult))
            print('Error writing position')
            print(self.getRxPacketError(error))
            return False
    
    def SyncRead(self, sts_ids):
        """
        Synchronized read from mutliple servos.
        Faster than reading from each servo independently.
        Also all reads are executed at the same time.

        :param sts_ids: Array of Servos to query data from

        :return: Returns array with information about each servo in form of [[sts_id, position, speed, moving],[...]]
        """
        
        dataArray = []
        
        for sts_id in sts_ids:
            addParamResult = self.groupSyncRead.addParam(sts_id)
            if addParamResult != True:
                print('Adding param for Servo ID ' + str(sts_id) + ' failed.')
        
        commResult = self.groupSyncRead.txRxPacket()
        if commResult != COMM_SUCCESS:
            print('Failure Sync Reading')
            print(self.getTxRxResult(commResult))
        
        for sts_id in sts_ids:
            returnData = [sts_id]
            data, error = self.groupSyncRead.isAvailable(sts_id, STS_PRESENT_POSITION_L, 11)
            if data == True:
                position = self.groupSyncRead.getData(sts_id, STS_PRESENT_POSITION_L, 2)
                speed = self.groupSyncRead.getData(sts_id, STS_PRESENT_SPEED_L, 2)
                moving = self.groupSyncRead.getData(sts_id, STS_MOVING, 1)
                
                returnData.append(position)
                returnData.append(speed)
                returnData.append(moving)
            
                print('Data for Servo ID: ' + str(sts_id))
                print('Position: ' + str(position))
                print('Speed: ' + str(self.sts_tohost(speed, 15)))
                print('Moving: ' + str(moving))
            else:
                print('GetData for groupSyncRead failed for Servo ID ' + str(sts_id))
            
            if error:
                print('Error checking isAvailable data')
                print(self.getRxPacketError(error))
            
            dataArray.append(returnData)
            
        self.groupSyncRead.clearParam()
        
        return dataArray
    
    def SyncWrite(self, sts_ids):
        """
        Synchronized write to  mutliple servos.
        Faster than writing a command to each servo independently.
        Also all actions are executed at the same time.

        :param sts_ids: Array of arrays in the form of [[sts_id, position, speed, acc],[...]]

        :return: Returns True if sync write was a success, False otherwise
        """
        for sts_id in sts_ids:
            id = sts_id[0]
            position = sts_id[1]
            speed = sts_id[2]
            acc = sts_id[3]
            
            txPacket = [acc, self.sts_lobyte(position), self.sts_hibyte(position), 0, 0, self.sts_lobyte(speed), self.sts_hibyte(speed)]
            addParamResult =  self.groupSyncWrite.addParam(id, txPacket)
            if addParamResult != True:
                print('Adding param for Servo ID ' + str(id) + ' failed.')
        
        commResult = self.groupSyncWrite.txPacket()
        if commResult != COMM_SUCCESS:
            print('Failure Sync Writing')
            print(self.getTxRxResult(commResult))
            self.groupSyncWrite.clearParam()
            return False
        else:
            self.groupSyncWrite.clearParam()
            print('Sync Write complete')
            return True
import machine as m  # for uart use
import utime  # for time control

# --------- INSTRUCTIONS -----
PING = 0x01
READ = 0x02
WRITE = 0x03
REG_WRITE = 0x04
ACTION = 0x05
RESET = 0x06
REBOOT = 0x08
STATUS = 0x55
SYNC_READ = 0x82
SYNC_WRITE = 0x83
BULK_READ = 0x92
BULK_WRITE = 0x93

# -------- EEPROM -------------
XL320_MODEL_NUMBER = 0
XL320_VER_FIRMWARE = 2
XL320_ID = 3
XL320_BAUD_RATE = 4
XL320_DELAY_TIME = 5
XL320_CW_ANGLE_LIMIT = 6  # min angle, default 0
XL320_CCW_ANGLE_LIMIT = 8  # max angle, default 300
XL320_CONTROL_MODE = 11  # joint or wheel mode, default joint (servo)
XL320_MAX_TORQUE = 15
XL320_RETURN_LEVEL = 17

# -------- RAM ----------------
XL320_TORQUE_ENABLE = 24  # servo mode on/off - turn into wheel
XL320_LED = 25
XL320_GOAL_POSITION = 30
XL320_GOAL_VELOCITY = 32
XL320_GOAL_TORQUE = 35
XL320_PRESENT_POSITION = 37  # current servo angle
XL320_PRESENT_SPEED = 39  # current speed
XL320_PRESENT_LOAD = 41  # current load
XL320_PRESENT_VOLTAGE = 45  # current voltage
XL320_PRESENT_TEMP = 46  # current temperature
XL320_MOVING = 49
XL320_HW_ERROR_STATUS = 50
XL320_PUNCH = 51

# --------- OTHER -------------
XL320_RESET_ALL = 0xFF
XL320_RESET_ALL_BUT_ID = 0x01
XL320_RESET_ALL_BUT_ID_BAUD_RATE = 0x02
XL320_LED_WHITE = 7
XL320_LED_BLUE_GREEN = 6
XL320_LED_PINK = 5
XL320_LED_BLUE = 4
XL320_LED_YELLOW = 3
XL320_LED_GREEN = 2
XL320_LED_RED = 1
XL320_LED_OFF = 0
XL320_BROADCAST_ADDR = 0xFE  # a packet with this ID will go to all servos
XL320_WHEEL_MODE = 1
XL320_JOINT_MODE = 2  # normal servo
XL320_9600 = 0  # 0: 9600, 1:57600, 2:115200, 3:1Mbps
XL320_57600 = 1
XL320_115200 = 2
XL320_1000000 = 3

# this table is needed in order to create the ultimate two values which correspond to only
# the checksum of protocol 2.0
crc_table = [
    0x0000,
    0x8005,
    0x800F,
    0x000A,
    0x801B,
    0x001E,
    0x0014,
    0x8011,
    0x8033,
    0x0036,
    0x003C,
    0x8039,
    0x0028,
    0x802D,
    0x8027,
    0x0022,
    0x8063,
    0x0066,
    0x006C,
    0x8069,
    0x0078,
    0x807D,
    0x8077,
    0x0072,
    0x0050,
    0x8055,
    0x805F,
    0x005A,
    0x804B,
    0x004E,
    0x0044,
    0x8041,
    0x80C3,
    0x00C6,
    0x00CC,
    0x80C9,
    0x00D8,
    0x80DD,
    0x80D7,
    0x00D2,
    0x00F0,
    0x80F5,
    0x80FF,
    0x00FA,
    0x80EB,
    0x00EE,
    0x00E4,
    0x80E1,
    0x00A0,
    0x80A5,
    0x80AF,
    0x00AA,
    0x80BB,
    0x00BE,
    0x00B4,
    0x80B1,
    0x8093,
    0x0096,
    0x009C,
    0x8099,
    0x0088,
    0x808D,
    0x8087,
    0x0082,
    0x8183,
    0x0186,
    0x018C,
    0x8189,
    0x0198,
    0x819D,
    0x8197,
    0x0192,
    0x01B0,
    0x81B5,
    0x81BF,
    0x01BA,
    0x81AB,
    0x01AE,
    0x01A4,
    0x81A1,
    0x01E0,
    0x81E5,
    0x81EF,
    0x01EA,
    0x81FB,
    0x01FE,
    0x01F4,
    0x81F1,
    0x81D3,
    0x01D6,
    0x01DC,
    0x81D9,
    0x01C8,
    0x81CD,
    0x81C7,
    0x01C2,
    0x0140,
    0x8145,
    0x814F,
    0x014A,
    0x815B,
    0x015E,
    0x0154,
    0x8151,
    0x8173,
    0x0176,
    0x017C,
    0x8179,
    0x0168,
    0x816D,
    0x8167,
    0x0162,
    0x8123,
    0x0126,
    0x012C,
    0x8129,
    0x0138,
    0x813D,
    0x8137,
    0x0132,
    0x0110,
    0x8115,
    0x811F,
    0x011A,
    0x810B,
    0x010E,
    0x0104,
    0x8101,
    0x8303,
    0x0306,
    0x030C,
    0x8309,
    0x0318,
    0x831D,
    0x8317,
    0x0312,
    0x0330,
    0x8335,
    0x833F,
    0x033A,
    0x832B,
    0x032E,
    0x0324,
    0x8321,
    0x0360,
    0x8365,
    0x836F,
    0x036A,
    0x837B,
    0x037E,
    0x0374,
    0x8371,
    0x8353,
    0x0356,
    0x035C,
    0x8359,
    0x0348,
    0x834D,
    0x8347,
    0x0342,
    0x03C0,
    0x83C5,
    0x83CF,
    0x03CA,
    0x83DB,
    0x03DE,
    0x03D4,
    0x83D1,
    0x83F3,
    0x03F6,
    0x03FC,
    0x83F9,
    0x03E8,
    0x83ED,
    0x83E7,
    0x03E2,
    0x83A3,
    0x03A6,
    0x03AC,
    0x83A9,
    0x03B8,
    0x83BD,
    0x83B7,
    0x03B2,
    0x0390,
    0x8395,
    0x839F,
    0x039A,
    0x838B,
    0x038E,
    0x0384,
    0x8381,
    0x0280,
    0x8285,
    0x828F,
    0x028A,
    0x829B,
    0x029E,
    0x0294,
    0x8291,
    0x82B3,
    0x02B6,
    0x02BC,
    0x82B9,
    0x02A8,
    0x82AD,
    0x82A7,
    0x02A2,
    0x82E3,
    0x02E6,
    0x02EC,
    0x82E9,
    0x02F8,
    0x82FD,
    0x82F7,
    0x02F2,
    0x02D0,
    0x82D5,
    0x82DF,
    0x02DA,
    0x82CB,
    0x02CE,
    0x02C4,
    0x82C1,
    0x8243,
    0x0246,
    0x024C,
    0x8249,
    0x0258,
    0x825D,
    0x8257,
    0x0252,
    0x0270,
    0x8275,
    0x827F,
    0x027A,
    0x826B,
    0x026E,
    0x0264,
    0x8261,
    0x0220,
    0x8225,
    0x822F,
    0x022A,
    0x823B,
    0x023E,
    0x0234,
    0x8231,
    0x8213,
    0x0216,
    0x021C,
    0x8219,
    0x0208,
    0x820D,
    0x8207,
    0x0202,
]

# header of the packet
HEADER = [0xFF, 0xFF, 0xFD, 0x00]

# xl320 class for servo control
class Servo(object):
    # constructor
    def __init__(self, dir_com, baudrate=1000000, serialid=1, tx_pin=4, rx_pin=5):

        self.baudrate = baudrate
        self.serialid = serialid
        self.dir_com = m.Pin(
            dir_com, m.Pin.OUT
        )  # a pin for the communication direction is defined
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin

        # uart object defined
        try:
            self.uart = m.UART(self.serialid, self.baudrate, tx=m.Pin(self.tx_pin), rx=m.Pin(self.rx_pin))
            # self.uart = m.UART(self.serialid, self.baudrate)
            self.uart.init(self.baudrate, bits=8, parity=None, stop=1)
        except Exception as e:
            print(e)

    # generic methods to send packet -> this is a list of values
    def sendPacket(self, packet):
        self.dir_com.value(1)

        try:
            self.uart.write(bytearray(packet))
            a = utime.ticks_us()  # start time counting
        except Exception as e:
            print(e)

        utime.sleep_us(325)  # this is a time specified experimentally
        self.dir_com.value(0)

        while True:
            msg = com.read()
            if msg is not None and (utime.ticks_us() - a) >= 1450:
                print(list(msg))
                return list(msg)
            if (utime.ticks_us() - a) >= 1450:
                break

    # --------------------------SPECIFIC WRITING METHODS------------------------------
    # ==================================EEPROM=========================================

    def set_control_mode(self, ID, mode):  # 1 (wheel), 2 (joint)
        comwrite(self.uart, self.dir_com, ID, XL320_CONTROL_MODE, [mode])

    def set_id(self, ID, newID):
        comwrite(self.uart, self.dir_com, ID, XL320_ID, [newID])

    def set_baudrate(self, ID, baudrate):
        comwrite(self.uart, self.dir_com, ID, XL320_BAUD_RATE, [baudrate])

    def set_cw_angle_limit(self, ID, angle):
        comwrite(
            self.uart,
            self.dir_com,
            ID,
            XL320_CW_ANGLE_LIMIT,
            le(int(angle / 300 * 1023)),
        )

    def set_ccw_angle_limit(self, ID, angle):
        comwrite(
            self.uart,
            self.dir_com,
            ID,
            XL320_CCW_ANGLE_LIMIT,
            le(int(angle / 300 * 1023)),
        )

    def set_max_torque(self, ID, torque):
        comwrite(self.uart, self.dir_com, ID, XL320_MAX_TORQUE, le(torque))

    # ========================RAM======================================================

    def torque_enable(
        self, ID, status
    ):  # default 0 (torque disabled), 1 (torque enabled), cuando torque enabled, eeprom es bloqueado
        comwrite(self.uart, self.dir_com, ID, XL320_TORQUE_ENABLE, [status])

    def goal_speed(self, ID, speed):
        comwrite(self.uart, self.dir_com, ID, XL320_GOAL_VELOCITY, le(speed))

    def goal_position(self, ID, position):
        comwrite(
            self.uart,
            self.dir_com,
            ID,
            XL320_GOAL_POSITION,
            le(int(position / 300 * 1023)),
        )

    def goal_torque(self, ID, torque):
        comwrite(self.uart, self.dir_com, ID, XL320_GOAL_TORQUE, le(1023))

    # ----------------------------SPECIFIC READING METHODS-----------------------------
    # ==================================EEPROM=========================================

    def read_model_number(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_MODEL_NUMBER, le(2))
        return word(data[-4], data[-3])

    def read_firmware(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_VER_FIRMWARE, le(1))
        return data[-3]

    def read_baudrate(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_BAUD_RATE, le(1))
        return data[-3]

    def read_delay_time(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_DELAY_TIME, le(1))
        return data[-3]

    def read_cw_angle_limit(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_CW_ANGLE_LIMIT, le(2))
        return word(data[-4], data[-3]) * 300 / 1023

    def read_ccw_angle_limit(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_CCW_ANGLE_LIMIT, le(2))
        return word(data[-4], data[-3]) * 300 / 1023

    def read_control_mode(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_CONTROL_MODE, le(1))
        return data[-3]

    def read_max_torque(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_MAX_TORQUE, le(2))
        return word(data[-4], data[-3])

    def read_return_level(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_RETURN_LEVEL, le(1))
        return data[-3]

    # =================================RAM===============================================
    def read_torque_enable(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_TORQUE_ENABLE, le(1))
        return data[-3]

    def read_goal_torque(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_GOAL_TORQUE, le(2))
        return word(data[-4], data[-3])

    def read_goal_position(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_GOAL_POSITION, le(2))
        return word(data[-4], data[-3]) * 300 / 1023

    def read_goal_speed(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_GOAL_VELOCITY, le(2))
        return word(data[-4], data[-3])

    def read_present_position(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_PRESENT_POSITION, le(2))
        return word(data[-4], data[-3]) * 300 / 1023

    def read_present_speed(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_PRESENT_SPEED, le(2))
        return word(data[-4], data[-3])

    def read_present_load(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_PRESENT_LOAD, le(2))
        return word(data[-4], data[-3])

    def read_present_voltage(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_PRESENT_VOLTAGE, le(1))
        return data[-3]

    def read_present_temperature(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_PRESENT_TEMP, le(1))
        return data[-3]

    def read_moving(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_MOVING, le(1))
        return data[-3]

    def read_hw_error_status(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_HW_ERROR_STATUS, le(1))
        return data[-3]

    def read_punch(self, ID):
        data = comread(self.uart, self.dir_com, ID, XL320_PUNCH, le(2))
        return word(data[-4], data[-3])

    # ================================OTHER METHODS====================================

    def reset_all(self, ID):
        comwrite(self.uart, self.dir_com, ID, [XL320_RESET_ALL])

    def reset_all_id(self, ID):
        comwrite(self.uart, self.dir_com, ID, [XL320_RESET_ALL_BUT_ID])

    def reset_all_id_baud(self, ID):
        comwrite(self.uart, self.dir_com, ID, [XL320_RESET_ALL_BUT_ID_BAUD_RATE])


# ===============================GENERIC METHODS==================================
# creacion del paquete de escritura y envio
# package creation, about write instruction
def comwrite(com, dir_com, ID, reg=None, params=None):
    dir_com.value(1)

    try:
        pkt = bytearray(makePacket(ID, WRITE, reg, params))
        com.write(pkt)
        a = utime.ticks_us()
    except Exception as e:
        print(e)

    utime.sleep_us(325)
    dir_com.value(0)

    while True:
        msg = com.read()
        if msg is not None:
            print(list(msg))
            return list(msg)
        if (utime.ticks_us() - a) >= 1450:
            break


# package creation, send and receive
def comread(com, dir_com, ID, reg, length):
    dir_com.value(1)

    try:
        pkt = bytearray(makePacket(ID, READ, reg, length))
        com.write(pkt)
    except Exception as e:
        print(e)

    utime.sleep_us(325)
    dir_com.value(0)
    a = utime.ticks_us()
    data = []

    while True:
        msg = com.read(13)

        if msg is not None:
            data += list(msg)

        try:
            if data[5] == (len(data) - 7):
                print(data)
                return data
        except:
            if (utime.ticks_us() - a) >= 2000:
                break


def makePacket(ID, instr, reg=None, params=None):
    """
	This makes a generic packet.
	TODO: look a struct ... does that add value using it?
	0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]
	in:
		ID - servo id
		instr - instruction
		reg - register
		params - instruction parameter values
	out: packet
	"""
    pkt = []
    pkt += HEADER  # header and reserved byte
    pkt += [ID]
    pkt += [0x00, 0x00]  # length placeholder
    pkt += [instr]  # instruction
    if reg:
        pkt += le(reg)  # not everything has a register
    if params:
        pkt += params  # not everything has parameters
    length = le(len(pkt) - 5)  # length = len(packet) - (header(3), reserve(1), id(1))
    pkt[5] = length[0]  # L
    pkt[6] = length[1]  # H
    crc = crc16(pkt)
    pkt += le(crc)
    print(pkt)
    return pkt


# util function?
def le(h):
    """
	Little-endian, takes a 16b number and returns an array arrange in little
	endian or [low_byte, high_byte].
	"""
    h &= 0xFFFF  # make sure it is 16 bits
    return [h & 0xFF, h >> 8]


def word(l, h):
    """
	Given a low and high bit, converts the number back into a word.
	"""
    return (h << 8) + l


def crc16(data_blk):
    """
	Calculate crc
	in: data_blk - entire packet except last 2 crc bytes
	out: crc_accum - 16 word
	"""
    data_blk_size = len(data_blk)
    crc_accum = 0
    for j in range(data_blk_size):
        i = ((crc_accum >> 8) ^ data_blk[j]) & 0xFF
        crc_accum = (crc_accum << 8) ^ crc_table[i]
        crc_accum &= 0xFFFF  # keep to 16 bits

    return crc_accum
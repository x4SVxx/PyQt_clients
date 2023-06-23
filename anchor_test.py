import socket

config = {
            "ip": "192.168.99.9",
            "number": 1,
            "adrx": 16492,
            "adtx": 16492,
            "x": 11.57,
            "y": 0.54,
            "z": 2.72,
            "role": "Master",
            "masternumber": 0,
            "lag": 2000
         }

rf_config = {
                "chnum": 2,
                "prf": 64,
                "datarate": 6.8,
                "preamblecode": 9,
                "preamblelen": 128,
                "pac": 16,
                "nsfd": 0,
                "diagnostic": 0,
                "lag": 20000

            }

class Anchor:
    def __init__(self, msg):
        self.IP = msg["ip"]
        self.number = msg["number"]
        self.x = msg["x"]
        self.y = msg["y"]
        self.z = msg["z"]
        self.ADRx = int(msg["adrx"])
        self.ADTx = int(msg["adtx"])
        self.Role = 1 if msg["role"] == "Master" else 0
        self.master_number = msg["masternumber"]
        self.lag = int(msg["lag"])

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.IP, 3000))
            self.socket.recv(3)
            data = self.socket.recv(500)
            msg = decode_anchor_message(data)
            print(msg)
            self.ID = msg["receiver"]
            self.name = str(hex(self.ID[1])[2:]) + str(hex(self.ID[0])[2:])
            print(f"ANCHOR {self.number} {self.name} CONNECTED")
        except:
            print(f"ANCHOR {self.number} NOT CONNECTED")

        self.data2sendflag = 0
        self.master = []
        self.master_ID = []
        self.master_name = []
        self.Range = []
        self.sync_flag = 0
        self.current_master_seq = -1
        self.current_rx = -1.
        self.current_tx = -1.
        self.X = []
        self.Dx = []
        self.rx_last_cs = -1.
        self.tx_last_cs = -1.
        self.startnumber = 5
        self.tx = []
        self.rx = []
        self.k_skip = 0


    def set_rf_config(self, rf_config):
        PRF = {
            16: 1,
            64: 2
        }
        DATARATE = {
            110: 0,
            850: 1,
            6.8: 2
        }
        PREAMBLE_LEN = {
            64: int(0x04),
            128: int(0x14),
            256: int(0x24),
            512: int(0x34),
            1024: int(0x08),
            1536: int(0x18),
            2048: int(0x28),
            4096: int(0x0C)
        }
        PAC = {
            8: 0,
            16: 1,
            32: 2,
            64: 3
        }
        RTLS_CMD_SET_CFG_CCP = build_RTLS_CMD_SET_CFG_CCP(self.Role,
                                                             rf_config["chnum"],
                                                             PRF[rf_config["prf"]],
                                                             DATARATE[rf_config["datarate"]],
                                                             rf_config["preamblecode"],
                                                             PREAMBLE_LEN[rf_config["preamblelen"]],
                                                             PAC[rf_config["pac"]],
                                                             rf_config["nsfd"],
                                                             self.ADRx,
                                                             self.ADTx,
                                                             rf_config["diagnostic"],
                                                             rf_config["lag"])
        try:
            self.socket.sendall(RTLS_CMD_SET_CFG_CCP)
            print("SET RF")
        except:
            print("ERROR SET RF_CONFIG ON ANCHOR" + str(self.IP))

    def start_spam(self):
        try:
            self.socket.sendall(build_RTLS_START_REQ(1))
        except:
            print("ERROR START SPAM ON ANCOR" + str(self.IP))

    def anchor_handler(self):
        while True:
            header = self.socket.recv(3)
            # try:
            numberofbytes = header[1]
            data = self.socket.recv(numberofbytes)
            ending = self.socket.recv(3)
            msg = decode_anchor_message(data)
            msg["receiver"] = self.ID
            msg["receiver"] = str(hex(msg["receiver"][1])[2:]) + str(hex(msg["receiver"][0])[2:])

            print(msg)
            # except:
            # print("NOTHING")


byteorder_def = 'little'

def build_RTLS_CMD_SET_CFG_CCP(M, CP, PRF, DR, PC, PL, PSN_L, PSN_U, ADRx, ADTx, LD, Lag):
    RTLS_CMD_SET_CFG_CCP_VALUE = 0x44
    mes = RTLS_CMD_SET_CFG_CCP_VALUE.to_bytes(1, byteorder=byteorder_def, signed=False)
    val = 0
    mes += val.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += M.to_bytes(1, byteorder=byteorder_def, signed=False)
    val = CP + PRF * pow(2, 4)
    mes += val.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += DR.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += PC.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += PL.to_bytes(1, byteorder=byteorder_def, signed=False)
    val = PSN_L + PSN_U * pow(2, 4)
    mes += val.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += ADRx.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += ADTx.to_bytes(2, byteorder=byteorder_def, signed=False)
    val = 0
    mes += val.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += LD.to_bytes(1, byteorder=byteorder_def, signed=False)
    val = 0
    mes += val.to_bytes(8, byteorder=byteorder_def, signed=False)
    mes += Lag.to_bytes(4, byteorder=byteorder_def, signed=False)

    return mes


def build_RTLS_START_REQ(ON_OFF):
    RTLS_START_REQ_VALUE = 0x57
    mes = RTLS_START_REQ_VALUE.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += ON_OFF.to_bytes(1, byteorder=byteorder_def, signed=False)
    return mes


def decode_anchor_message(data):
    FnCE = data[0]
    msg = {}
    if FnCE == 49:  # 0x31
        msg["type"] = "CS_RX"
        msg["sender"] = data[2:10]
        msg["receiver"] = []
        msg["seq"] = data[1]
        msg["timestamp"] = int.from_bytes(data[10:15], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
    elif FnCE == 50:  # 0x32 COMPATIBLE
        msg["type"] = "BLINK"
        msg["sender"] = data[2:10]
        msg["receiver"] = []
        msg["sn"] = data[1]
        msg["state"] = []
        msg["timestamp"] = int.from_bytes(data[10:15], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
        msg["tx_timestamp"] = []
    elif FnCE == 48:  # 0x30
        msg["type"] = "CS_TX"
        msg["sender"] = []
        msg["receiver"] = []
        msg["seq"] = data[1]
        msg["timestamp"] = int.from_bytes(data[2:7], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
    elif FnCE == 52:  # 0x34 TX_TS
        msg["type"] = "BLINK"
        msg["sender"] = data[2:10]
        msg["receiver"] = []
        msg["sn"] = data[1]
        msg["state"] = data[20]
        msg["timestamp"] = int.from_bytes(data[10:15], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
        msg["tx_timestamp"] = int.from_bytes(data[15:20], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
    elif FnCE == 53:  # 0x35 SHORT
        msg["type"] = "BLINK"
        msg["sender"] = data[2:10]
        msg["receiver"] = []
        msg["sn"] = data[1]
        msg["state"] = data[15]
        msg["timestamp"] = int.from_bytes(data[10:15], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
        msg["tx_timestamp"] = []
    elif FnCE == 66:  # 0x42
        msg["type"] = "Config request"
        msg["receiver"] = data[1:9]
    else:
        msg["type"] = "Unknown"
    return msg


if __name__ == "__main__":
    anchor = Anchor(config)
    anchor.set_rf_config(rf_config)
    anchor.start_spam()
    anchor.anchor_handler()
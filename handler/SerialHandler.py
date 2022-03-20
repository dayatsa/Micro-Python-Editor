from serial.tools.list_ports import comports


class SerialHandler:

    @staticmethod
    def get_list_ports():
        # Find and return a list of all EiBotBoard units
        # connected via USB port.
        try:
            from serial.tools.list_ports import comports
        except ImportError():
            return ["NONE".ljust(20)]
            print("import error")
        
        if comports:
            com_ports_list = list(comports())
            # print(com_ports_list)
            ebb_ports_list = []
            for port in com_ports_list:
                port_has_ebb = False
                if port[1].startswith("USB"):
                    port_has_ebb = True
                elif port[2].startswith("USB VID:PID"):
                    port_has_ebb = True
                if port_has_ebb:
                    ebb_ports_list.append(port[0].ljust(20))
            if len(ebb_ports_list) == 0:
                return ['NONE'.ljust(20)]
            else:
                return ebb_ports_list 
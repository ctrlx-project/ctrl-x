from pymetasploit3.msfrpc import MsfRpcClient
from parse_scan import parse_from_JSON
from sys import argv

my_ip = "0.0.0.0"

class MetasploitManager:
    def __init__(self):
        self.parsed_scan = None
        self.manager = MsfRpcClient('Ko4jSliH', port=55552)

    def update_scan(parsed_scan: dict):
        self.parsed_scan = parsed_scan 

    def analyze_targets(self):
        """Find useful modules from Metasploit manager based on CVE in parsed_scan 
        and fill the missing required option using the information stored in parsed_scan"""
        for ip, value in self.parsed_scan.items():
            if value["state"] != "up":
                continue
            for port, info in value["ports"].items():
                cve_set = info.get("vulner")
                for cve in cve_set:
                    analyze_vulnerability(ip, port, cve)

    def analyze_vulnerability(ip: str, port: str, cve: str):
        module_list = self.manager.modules.search(cve)
        for module in module_list:
            if module and module.get("fullname") and module.get("type") == "exploit":
                exploit = self.manager.modules.use(module.get("type"), module.get("fullname"))
                missing = exploit.missing_required
                print("Missing at the start: ", exploit.missing_required)
                for option in missing:
                    exploit[option] = fill_option(option, ip, port, my_ip)
                print("Missing at the end: ", exploit.missing_required)

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
    


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_metasploit.py <file>; e.g. py parse_metasploit.py seed/10.1.0.1.json")
        exit(1)
    result = parse_from_JSON(argv[1])
    
    metasploit_hosts(result)
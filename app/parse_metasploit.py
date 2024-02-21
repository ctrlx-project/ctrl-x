from pymetasploit3.msfrpc import MsfRpcClient
from parse_scan import parse_from_JSON
from sys import argv


my_ip = "0.0.0.0"


def fill_option(option_name:str, target_ip:str, target_port:int, my_ip: str)->str | int:
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
    


def metasploit_hosts(parsed_scan:dict, manager:MsfRpcClient):
    """Find useful modules from Metasploit manager based on CVE in parsed_scan 
    and fill the missing required option using the information stored in parsed_scan"""
    for ip, value in parsed_scan.items():
        if value["state"] != "up":
            continue
        for port, info in value["ports"].items():
            cve_set = info.get("vulner")
            if cve_set:
                for cve in cve_set:
                    module_list = manager.modules.search(cve)
                    for module in module_list:
                        if module and module.get("fullname") and module.get("type"):
                            exploit = manager.modules.use(module.get("type"), module.get("fullname"))
                            missing = exploit.missing_required
                            print("Missing at the start: ", exploit.missing_required)
                            for option in missing:
                                exploit[option] = fill_option(option, ip, port, my_ip)
                            print("Missing at the end: ", exploit.missing_required)


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_metasploit.py <file>; e.g. py parse_metasploit.py seed/10.1.0.1.json")
        exit(1)
    result = parse_from_JSON(argv[1])
    manager = MsfRpcClient('Ko4jSliH', port=55552)
    metasploit_hosts(result, manager)
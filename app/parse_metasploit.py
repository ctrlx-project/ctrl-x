from pymetasploit3.msfrpc import MsfRpcClient
from parse_scan import parse_from_JSON
from sys import argv


myIP = "0.0.0.0"


def metasploit_hosts(parsed_scan, manager):
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
                            for option in missing:
                                option_upper = option.upper()
                                if option_upper == "RHOSTS" or option_upper == "RHOST":
                                    exploit[option] = ip
                                elif option_upper == "SRVHOST":
                                    exploit[option] = myIP
                            # print("Missing at the end: ", exploit.missing_required)


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_metasploit.py <file>; e.g. py parse_metasploit.py seed/10.1.0.1.json")
        exit(1)
    result = parse_from_JSON(argv[1])
    manager = MsfRpcClient('Bz1evBuV', port=55552)
    metasploit_hosts(result, manager)
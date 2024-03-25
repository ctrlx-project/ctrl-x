"""
I'm not sure exactly what tests will look like, but I'm starting writting the unit tests for the exploit and maybe parser modules.
"""

import parse_scan
import json, pprint

SCAN_PATH = "seed/nmap/metasploitable_scan.json"

with open(SCAN_PATH) as json_file:
    SCAN = json.load(json_file)

def test_load_json():
    loaded_json = parse_scan.loadJSON(SCAN_PATH)
    print(loaded_json == SCAN)

def test_get_cve():
    expected_cves = {'CVE-2009-1890', 'CVE-2016-5387', 'CVE-2011-3639',
                     'CVE-2009-3094', 'CVE-2012-2687', 'CVE-2012-0883',
                     'CVE-2008-2364', 'CVE-2008-0455', 'CVE-2014-0098',
                     'CVE-2009-3560', 'CVE-2014-0118', 'CVE-2009-1956',
                     'CVE-2014-0231', 'CVE-2011-3368', 'CVE-2010-0408',
                     'CVE-2009-1195', 'CVE-2012-4558', 'CVE-2008-0456',
                     'CVE-2011-3192', 'CVE-2017-9798', 'CVE-2008-2939',
                     'CVE-2017-7679', 'CVE-2017-3167', 'CVE-2009-3555',
                     'CVE-2010-1623', 'CVE-2012-3499', 'CVE-2007-6750',
                     'CVE-2013-1896', 'CVE-2015-3183', 'CVE-2017-9788',
                     'CVE-2013-1862', 'CVE-2013-5704', 'CVE-2014-0226',
                     'CVE-2010-1452', 'CVE-2009-3095', 'CVE-2009-2699',
                     'CVE-2016-4975', 'CVE-2016-8743', 'CVE-2010-0434',
                     'CVE-2013-6438', 'CVE-2008-0005', 'CVE-2011-441',
                     'CVE-2009-1891', 'CVE-2011-4415', 'CVE-2012-0053',
                     'CVE-2011-4317', 'CVE-2009-0023', 'CVE-2011-3607',
                     'CVE-2012-0031'}
    cves = parse_scan.get_CVE(SCAN["scan"]["10.10.0.14"]["tcp"]["80"]["script"]["vulners"])
    print(cves == expected_cves)

def test_parse_scan():
    # Will replace this line with database
    expected_result = {'10.10.0.14': {'state': 'up', 'ports': {'21': {'transport_protocol': 'tcp', 'name': 'ftp', 'service': 'vsftpd 2.3.4', 'vulner': {'CVE-2011-2523'}}, '22': {'transport_protocol': 'tcp', 'name': 'ssh', 'service': 'OpenSSH 4.7p1 Debian 8ubuntu1', 'vulner': {'CVE-2012-0814', 'CVE-2008-1657', 'CVE-2010-4754', 'CVE-2010-5107', 'CVE-2011-2168', 'CVE-2010-4478', 'CVE-2011-4327', 'CVE-2011-1013', 'CVE-2010-4755', 'CVE-2008-3259', 'CVE-2011-5000', 'CVE-2008-5161'}}, '23': {'transport_protocol': 'tcp', 'name': 'telnet', 'service': 'Linux telnetd'}, '25': {'transport_protocol': 'tcp', 'name': 'smtp', 'service': 'Postfix smtpd'}, '53': {'transport_protocol': 'tcp', 'name': 'domain', 'service': 'ISC BIND 9.4.2', 'vulner': {'CVE-2017-3141', 'CVE-2020-8617', 'CVE-2012-1033', 'CVE-2021-25219', 'CVE-2015-8705', 'CVE-2020-8622', 'CVE-2012-1667', 'CVE-2010-3614', 'CVE-2016-2775', 'CVE-2010-0290', 'CVE-2016-6170', 'CVE-2016-1285', 'CVE-2016-8864', 'CVE-2011-4313', 'CVE-2009-0696', 'CVE-2016-2848', 'CVE-2014-8500', 'CVE-2011-1910', 'CVE-2009-0265', 'CVE-2015-8461', 'CVE-2023-3341', 'CVE-2012-4244', 'CVE-2008-4163', 'CVE-2015-8704', 'CVE-2017-3145', 'CVE-2009-4022', 'CVE-2020-8616', 'CVE-2012-5166', 'CVE-2010-0382', 'CVE-2010-0097', 'CVE-2012-3817', 'CVE-2022-2795', 'CVE-2009-0025', 'CVE-2017-3142', 'CVE-2016-9444', 'CVE-2021-25215', 'CVE-2016-9131', 'CVE-2021-25216', 'CVE-2016-1286', 'CVE-2017-3143', 'CVE-2008-0122', 'CVE-2015-8000'}}, '80': {'transport_protocol': 'tcp', 'name': 'http', 'service': 'Apache httpd 2.2.8', 'vulner': {'CVE-2011-4317', 'CVE-2009-1890', 'CVE-2011-3639', 'CVE-2013-1896', 'CVE-2017-9798', 'CVE-2009-3094', 'CVE-2011-441', 'CVE-2009-1956', 'CVE-2017-9788', 'CVE-2008-2364', 'CVE-2011-3607', 'CVE-2010-1623', 'CVE-2016-8743', 'CVE-2009-3560', 'CVE-2009-3095', 'CVE-2013-6438', 'CVE-2014-0226', 'CVE-2007-6750', 'CVE-2012-0031', 'CVE-2010-0434', 'CVE-2010-1452', 'CVE-2014-0231', 'CVE-2011-3368', 'CVE-2009-1891', 'CVE-2012-0053', 'CVE-2012-4558', 'CVE-2015-3183', 'CVE-2008-2939', 'CVE-2012-3499', 'CVE-2014-0118', 'CVE-2017-3167', 'CVE-2014-0098', 'CVE-2009-3555', 'CVE-2009-0023', 'CVE-2009-1195', 'CVE-2008-0455', 'CVE-2017-7679', 'CVE-2010-0408', 'CVE-2011-3192', 'CVE-2013-1862', 'CVE-2013-5704', 'CVE-2016-4975', 'CVE-2008-0005', 'CVE-2016-5387', 'CVE-2009-2699', 'CVE-2008-0456', 'CVE-2012-2687', 'CVE-2011-4415', 'CVE-2012-0883'}}, '111': {'transport_protocol': 'tcp', 'name': 'rpcbind'}, '139': {'transport_protocol': 'tcp', 'name': 'netbios-ssn', 'service': 'Samba smbd 3.X - 4.X'}, '445': {'transport_protocol': 'tcp', 'name': 'netbios-ssn', 'service': 'Samba smbd 3.X - 4.X'}, '512': {'transport_protocol': 'tcp', 'name': 'exec', 'service': 'netkit-rsh rexecd'}, '513': {'transport_protocol': 'tcp', 'name': 'login', 'service': 'OpenBSD or Solaris rlogind'}, '514': {'transport_protocol': 'tcp', 'name': 'tcpwrapped'}, '1099': {'transport_protocol': 'tcp', 'name': 'java-rmi', 'service': 'GNU Classpath grmiregistry'}, '1524': {'transport_protocol': 'tcp', 'name': 'bindshell', 'service': 'Metasploitable root shell'}, '2049': {'transport_protocol': 'tcp', 'name': 'nfs'}, '2121': {'transport_protocol': 'tcp', 'name': 'ftp', 'service': 'ProFTPD 1.3.1', 'vulner': {'CVE-2009-3639', 'CVE-2011-4130', 'CVE-2010-4652', 'CVE-2021-46854', 'CVE-2017-7418', 'CVE-2009-0543', 'CVE-2009-0542', 'CVE-2023-51713', 'CVE-2011-1137', 'CVE-2010-3867', 'CVE-2016-3125', 'CVE-2008-4242', 'CVE-2019-12815', 'CVE-2019-19271', 'CVE-2012-609', 'CVE-2008-7265', 'CVE-2019-18217', 'CVE-2019-19272', 'CVE-2020-9272', 'CVE-2012-6095', 'CVE-2019-19270'}}, '3306': {'transport_protocol': 'tcp', 'name': 'mysql', 'service': 'MySQL 5.0.51a-3ubuntu5', 'vulner': {'CVE-2012-0102', 'CVE-2010-3838', 'CVE-2009-2446', 'CVE-2010-3836', 'CVE-2009-5026', 'CVE-2010-3837', 'CVE-2010-3834', 'CVE-2008-2079', 'CVE-2012-0087', 'CVE-2008-3963', 'CVE-2008-7247', 'CVE-2010-1849', 'CVE-2010-3677', 'CVE-2012-007', 'CVE-2009-4484', 'CVE-2008-0226', 'CVE-2009-4028', 'CVE-2010-3682', 'CVE-2009-4019', 'CVE-2012-4452', 'CVE-2012-0101', 'CVE-2012-0490', 'CVE-2008-4098', 'CVE-2012-0114', 'CVE-2010-1850', 'CVE-2012-0075', 'CVE-2010-1848', 'CVE-2010-1626', 'CVE-2012-0484', 'CVE-2010-3833'}}, '5432': {'transport_protocol': 'tcp', 'name': 'postgresql', 'service': 'PostgreSQL DB 8.3.0 - 8.3.7', 'vulner': {'CVE-2009-4034', 'CVE-2010-1975', 'CVE-2013-1900', 'CVE-2009-3231', 'CVE-2010-1170', 'CVE-2014-0060', 'CVE-2009-4136', 'CVE-2012-0868', 'CVE-2014-0065', 'CVE-2010-073', 'CVE-2012-0866', 'CVE-2010-1169', 'CVE-2013-1903', 'CVE-2014-0062', 'CVE-2013-1902', 'CVE-2010-3433', 'CVE-2014-0064', 'CVE-2013-0255', 'CVE-2014-0061', 'CVE-2009-3229', 'CVE-2014-0067', 'CVE-2011-2483', 'CVE-2014-0066', 'CVE-2010-0733', 'CVE-2010-4015', 'CVE-2012-0867', 'CVE-2012-3489', 'CVE-2009-0922', 'CVE-2012-2655', 'CVE-2012-3488', 'CVE-2010-1447', 'CVE-2014-0063', 'CVE-2009-3230', 'CVE-2012-2143', 'CVE-2010-0442'}}, '5900': {'transport_protocol': 'tcp', 'name': 'vnc', 'service': 'VNC'}, '6000': {'transport_protocol': 'tcp', 'name': 'X11'}, '6667': {'transport_protocol': 'tcp', 'name': 'irc', 'service': 'UnrealIRCd'}, '8009': {'transport_protocol': 'tcp', 'name': 'ajp13', 'service': 'Apache Jserv'}, '8180': {'transport_protocol': 'tcp', 'name': 'http', 'service': 'Apache Tomcat/Coyote JSP engine 1.1', 'vulner': {'CVE-2023-26044', 'CVE-2022-36032'}}}}}
    result = parse_scan.parse_scan(SCAN)
    print(expected_result == result)

pprint.pprint(parse_scan.parse_scan(SCAN))
with open("seed/scan_parser/parsed_metasploitable.json", 'w') as fp:
    json.dump(parse_scan.parse_scan(SCAN), fp)
test_load_json()
test_get_cve()
test_parse_scan()
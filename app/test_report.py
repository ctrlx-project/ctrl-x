from report import loadJSON, getDescription, descriptionToMD

def test_report():
    vulnerabilities = loadJSON("./app/seed/test_report/test.json")
    assert vulnerabilities == {
    "vsftpd 2.3.4":{
        "exploit":"exploit/unix/ftp/vsftpd_234_backdoor",
        "exploit_description":"This module exploits a malicious backdoor that was added to the VSFTPD download archive. This backdoor was introduced into the vsftpd-2.3.4.tar.gz archive between June 30th 2011 and July 1st 2011 according to the most recent information available. This backdoor was removed on July 3rd 2011.",
        "status":"ACQUIRED_SHELL",
        "payload":"cmd/unix/interact",
        "payload_description":"Interacts with a shell on an established socket connection",
        "exploit_options":{
        "WfsDelay":2,
        "RHOSTS":"10.10.0.14",
        "RPORT":"21",
        "SSLVersion":"Auto",
        "SSLVerifyMode":"PEER",
        "CPORT":49769,
        "CHOST":"10.10.0.13",
        "ConnectTimeout":10
        },
        "payload_options":{
        "CreateSession":True,
        "AutoVerifySession":True
        }
    },
    "CVE-2009-4484":{
             "exploit":"exploit/linux/mysql/mysql_yassl_getname",
             "exploit_description":"This module exploits a stack buffer overflow in the yaSSL (1.9.8 and earlier) implementation bundled with MySQL. By sending a specially crafted client certificate, an attacker can execute arbitrary code. This vulnerability is present within the CertDecoder::GetName function inside \"taocrypt/src/asn.cpp\". However, the stack buffer that is written to exists within a parent function's stack frame. NOTE: This vulnerability requires a non-default configuration. First, the attacker must be able to pass the host-based authentication. Next, the server must be configured to listen on an accessible network interface. Lastly, the server must have been manually configured to use SSL. The binary from version 5.5.0-m2 was built with /GS and /SafeSEH. During testing on Windows XP SP3, these protections successfully prevented exploitation. Testing was also done with mysql on Ubuntu 9.04. Although the vulnerable code is present, both version 5.5.0-m2 built from source and version 5.0.75 from a binary package were not exploitable due to the use of the compiler's FORTIFY feature. Although suse11 was mentioned in the original blog post, the binary package they provide does not contain yaSSL or support SSL.",
             "status":"NO_SHELL",
             "CVE":"CVE-2009-4484",
             "payload":"generic/custom",
             "payload_description":"Use custom string or file as payload. Set either PAYLOADFILE or PAYLOADSTR.",
             "exploit_options":{
                "WfsDelay":2,
                "RHOSTS":"10.10.0.14",
                "RPORT":"3306",
                "SSLVersion":"Auto",
                "SSLVerifyMode":"PEER",
                "CPORT":48383,
                "CHOST":"10.10.0.13",
                "ConnectTimeout":10
             },
             "payload_options":{
                
             }
          }
    }
    descriptions, CVSS, table = getDescription(vulnerabilities)
    target_table = """\n| Exploit Name | exploit/unix/ftp/vsftpd_234_backdoor |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 21 |
| SSLVersion | Auto |
| SSLVerifyMode | PEER |
| CPORT | 49769 |
| CHOST | 10.10.0.13 |
| ConnectTimeout | 10 |

| Payload Name | cmd/unix/interact |
| --- | --- |
| Payload Description | Interacts with a shell on an established socket connection |
| CreateSession | True |
| AutoVerifySession | True |\n\n"""

    assert table[0] == target_table
    assert descriptions == ["This module exploits a malicious backdoor that was added to the VSFTPD download archive. This backdoor was introduced into the vsftpd-2.3.4.tar.gz archive between June 30th 2011 and July 1st 2011 according to the most recent information available. This backdoor was removed on July 3rd 2011.", "Multiple stack-based buffer overflows in the CertDecoder::GetName function in src/asn.cpp in TaoCrypt in yaSSL before 1.9.9, as used in mysqld in MySQL 5.0.x before 5.0.90, MySQL 5.1.x before 5.1.43, MySQL 5.5.x through 5.5.0-m2, and other products, allow remote attackers to execute arbitrary code or cause a denial of service (memory corruption and daemon crash) by establishing an SSL connection and sending an X.509 client certificate with a crafted name field, as demonstrated by mysql_overflow1.py and the vd_mysql5 module in VulnDisco Pack Professional 8.11. NOTE: this was originally reported for MySQL 5.0.51a."]
    assert CVSS == [[None, None, None], ["CVE-2009-4484", 7.5, "AV:N/AC:L/Au:N/C:P/I:P/A:P"]]
    markdown = descriptionToMD(descriptions, CVSS, table)
    target_markdown = """This module exploits a malicious backdoor that was added to the VSFTPD download archive. This backdoor was introduced into the vsftpd-2.3.4.tar.gz archive between June 30th 2011 and July 1st 2011 according to the most recent information available. This backdoor was removed on July 3rd 2011.

| Exploit Name | exploit/unix/ftp/vsftpd_234_backdoor |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 21 |
| SSLVersion | Auto |
| SSLVerifyMode | PEER |
| CPORT | 49769 |
| CHOST | 10.10.0.13 |
| ConnectTimeout | 10 |

| Payload Name | cmd/unix/interact |
| --- | --- |
| Payload Description | Interacts with a shell on an established socket connection |
| CreateSession | True |
| AutoVerifySession | True |

Multiple stack-based buffer overflows in the CertDecoder::GetName function in src/asn.cpp in TaoCrypt in yaSSL before 1.9.9, as used in mysqld in MySQL 5.0.x before 5.0.90, MySQL 5.1.x before 5.1.43, MySQL 5.5.x through 5.5.0-m2, and other products, allow remote attackers to execute arbitrary code or cause a denial of service (memory corruption and daemon crash) by establishing an SSL connection and sending an X.509 client certificate with a crafted name field, as demonstrated by mysql_overflow1.py and the vd_mysql5 module in VulnDisco Pack Professional 8.11. NOTE: this was originally reported for MySQL 5.0.51a.
* Its CVE number is CVE-2009-4484.
* Its CVSS score is 7.5.
* Its CVSS vector is AV:N/AC:L/Au:N/C:P/I:P/A:P

| Exploit Name | exploit/linux/mysql/mysql_yassl_getname |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 3306 |
| SSLVersion | Auto |
| SSLVerifyMode | PEER |
| CPORT | 48383 |
| CHOST | 10.10.0.13 |
| ConnectTimeout | 10 |

| Payload Name | generic/custom |
| --- | --- |
| Payload Description | Use custom string or file as payload. Set either PAYLOADFILE or PAYLOADSTR. |

"""
    for i in range(len(markdown)):
        if markdown[i] != target_markdown[i]:
            print(i)
            print(ord(markdown[i]))
            print(markdown[i-10:i+10])
            print(ord(target_markdown[i]))
            print(target_markdown[i-10:i+10])
            break
    assert markdown == target_markdown

test_report()
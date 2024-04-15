from report import loadJSON, getDescription, descriptionToMD


def test_getDescription(vulnerabilities:dict)->tuple[list, list, list]:
    # Test getDescription from report.py
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
    return descriptions, CVSS, table


def test_report():
    # Test descriptionToMD from report.py
    vulnerabilities = loadJSON("./app/seed/test_report/test.json")
    descriptions, CVSS, table = test_getDescription(vulnerabilities)
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
# Vulnerabilities
* The mod_cgid module in the Apache HTTP Server before 2.4.10 does not have a timeout mechanism, which allows remote attackers to cause a denial of service (process hang) via a request to a CGI script that does not read from its stdin file descriptor.
	* Its CVE number is CVE-2014-0231.
	* Its CVSS score is 5.0.
	* Its CVSS vector is AV:N/AC:L/Au:N/C:N/I:N/A:P
* The mod_deflate module in Apache httpd 2.2.11 and earlier compresses large files until completion even after the associated network connection is closed, which allows remote attackers to cause a denial of service (CPU consumption).
	* Its CVE number is CVE-2009-1891.
	* Its CVSS score is 7.1.
	* Its CVSS vector is AV:N/AC:M/Au:N/C:N/I:N/A:C
* Multiple cross-site scripting (XSS) vulnerabilities in the make_variant_list function in mod_negotiation.c in the mod_negotiation module in the Apache HTTP Server 2.4.x before 2.4.3, when the MultiViews option is enabled, allow remote attackers to inject arbitrary web script or HTML via a crafted filename that is not properly handled during construction of a variant list.
	* Its CVE number is CVE-2012-2687.
	* Its CVSS score is 2.6.
	* Its CVSS vector is AV:N/AC:H/Au:N/C:N/I:P/A:N
* The ap_proxy_ftp_handler function in modules/proxy/proxy_ftp.c in the mod_proxy_ftp module in the Apache HTTP Server 2.0.63 and 2.2.13 allows remote FTP servers to cause a denial of service (NULL pointer dereference and child process crash) via a malformed reply to an EPSV command.
	* Its CVE number is CVE-2009-3094.
	* Its CVSS score is 2.6.
	* Its CVSS vector is AV:N/AC:H/Au:N/C:N/I:N/A:P
* Possible CRLF injection allowing HTTP response splitting attacks for sites which use mod_userdir. This issue was mitigated by changes made in 2.4.25 and 2.2.32 which prohibit CR or LF injection into the "Location" or other outbound header key or value. Fixed in Apache HTTP Server 2.4.25 (Affected 2.4.1-2.4.23). Fixed in Apache HTTP Server 2.2.32 (Affected 2.2.0-2.2.31).
	* Its CVE number is CVE-2016-4975.
	* Its CVSS score is 6.1.
	* Its CVSS vector is CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N
* In Apache httpd 2.2.x before 2.2.33 and 2.4.x before 2.4.26, use of the ap_get_basic_auth_pw() by third-party modules outside of the authentication phase may lead to authentication requirements being bypassed.
	* Its CVE number is CVE-2017-3167.
	* Its CVSS score is 9.8.
	* Its CVSS vector is CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
* The dav_xml_get_cdata function in main/util.c in the mod_dav module in the Apache HTTP Server before 2.4.8 does not properly remove whitespace characters from CDATA sections, which allows remote attackers to cause a denial of service (daemon crash) via a crafted DAV WRITE request.
	* Its CVE number is CVE-2013-6438.
	* Its CVSS score is 5.0.
	* Its CVSS vector is AV:N/AC:L/Au:N/C:N/I:N/A:P
* Multiple cross-site scripting (XSS) vulnerabilities in the balancer_handler function in the manager interface in mod_proxy_balancer.c in the mod_proxy_balancer module in the Apache HTTP Server 2.2.x before 2.2.24-dev and 2.4.x before 2.4.4 allow remote attackers to inject arbitrary web script or HTML via a crafted string.
	* Its CVE number is CVE-2012-4558.
	* Its CVSS score is 4.3.
	* Its CVSS vector is AV:N/AC:M/Au:N/C:N/I:P/A:N
* Off-by-one error in the apr_brigade_vprintf function in Apache APR-util before 1.3.5 on big-endian platforms allows remote attackers to obtain sensitive information or cause a denial of service (application crash) via crafted input.
	* Its CVE number is CVE-2009-1956.
	* Its CVSS score is 6.4.
	* Its CVSS vector is AV:N/AC:L/Au:N/C:P/I:N/A:P
* scoreboard.c in the Apache HTTP Server 2.2.21 and earlier might allow local users to cause a denial of service (daemon crash during shutdown) or possibly have unspecified other impact by modifying a certain type field within a scoreboard shared memory segment, leading to an invalid call to the free function.
	* Its CVE number is CVE-2012-0031.
	* Its CVSS score is 4.6.
	* Its CVSS vector is AV:L/AC:L/Au:N/C:P/I:P/A:P
* The log_cookie function in mod_log_config.c in the mod_log_config module in the Apache HTTP Server before 2.4.8 allows remote attackers to cause a denial of service (segmentation fault and daemon crash) via a crafted cookie that is not properly handled during truncation.
	* Its CVE number is CVE-2014-0098.
	* Its CVSS score is 5.0.
	* Its CVSS vector is AV:N/AC:L/Au:N/C:N/I:N/A:P
* envvars (aka envvars-std) in the Apache HTTP Server before 2.4.2 places a zero-length directory name in the LD_LIBRARY_PATH, which allows local users to gain privileges via a Trojan horse DSO in the current working directory during execution of apachectl.
	* Its CVE number is CVE-2012-0883.
	* Its CVSS score is 6.9.
	* Its CVSS vector is AV:L/AC:M/Au:N/C:C/I:C/A:C
* mod_dav.c in the Apache HTTP Server before 2.2.25 does not properly determine whether DAV is enabled for a URI, which allows remote attackers to cause a denial of service (segmentation fault) via a MERGE request in which the URI is configured for handling by the mod_dav_svn module, but a certain href attribute in XML data refers to a non-DAV URI.
	* Its CVE number is CVE-2013-1896.
	* Its CVSS score is 4.3.
	* Its CVSS vector is AV:N/AC:M/Au:N/C:N/I:N/A:P
* The deflate_in_filter function in mod_deflate.c in the mod_deflate module in the Apache HTTP Server before 2.4.10, when request body decompression is enabled, allows remote attackers to cause a denial of service (resource consumption) via crafted request data that decompresses to a much larger size.
	* Its CVE number is CVE-2014-0118.
	* Its CVSS score is 4.3.
	* Its CVSS vector is AV:N/AC:M/Au:N/C:N/I:N/A:P
* protocol.c in the Apache HTTP Server 2.2.x through 2.2.21 does not properly restrict header information during construction of Bad Request (aka 400) error documents, which allows remote attackers to obtain the values of HTTPOnly cookies via vectors involving a (1) long or (2) malformed header in conjunction with crafted web script.
	* Its CVE number is CVE-2012-0053.
	* Its CVSS score is 4.3.
	* Its CVSS vector is AV:N/AC:M/Au:N/C:P/I:N/A:N
* Memory leak in the apr_brigade_split_line function in buckets/apr_brigade.c in the Apache Portable Runtime Utility library (aka APR-util) before 1.3.10, as used in the mod_reqtimeout module in the Apache HTTP Server and other software, allows remote attackers to cause a denial of service (memory consumption) via unspecified vectors related to the destruction of an APR bucket.
	* Its CVE number is CVE-2010-1623.
	* Its CVSS score is 5.0.
	* Its CVSS vector is AV:N/AC:L/Au:N/C:N/I:N/A:P

# Potential Impacts
---
**Vulnerability 1: Denial of Service via CGI Script**
* Remote attackers can cause a denial of service by sending a request to a CGI script that does not read from its stdin file descriptor.

**Vulnerability 2: Denial of Service via CPU Consumption**
* Remote attackers can cause a denial of service by compressing large files until completion even after the associated network connection is closed.

**Vulnerability 3: Cross-Site Scripting (XSS)**
* Remote attackers can inject arbitrary web script or HTML via a crafted filename that is not properly handled during construction of a variant list.

**Vulnerability 4: Denial of Service via FTP Server**
* Remote attackers can cause a denial of service by sending a malformed reply to an EPSV command to an FTP server.

**Vulnerability 5: CRLF Injection**
* Remote attackers can perform HTTP response splitting attacks by injecting arbitrary web script or HTML into the "Location" or other outbound header key or value.

**Vulnerability 6: Authentication Bypass**
* Third-party modules outside of the authentication phase may bypass authentication requirements if ap_get_basic_auth_pw() is used.

**Vulnerability 7: Cross-Site Scripting (XSS)**
* Remote attackers can inject arbitrary web script or HTML via crafted string in balancer_handler function.

**Vulnerability 8: Cross-Site Scripting (XSS)**
* Remote attackers can inject arbitrary web script or HTML via crafted input in scoreboard.c.

**Vulnerability 9: Denial of Service via LD_LIBRARY_PATH**
* Remote attackers can gain privileges by placing a zero-length directory name in the LD_LIBRARY_PATH.

**Vulnerability 10: Denial of Service via HTTPOnly Cookie**
* Remote attackers can obtain the values of HTTPOnly cookies via vectors involving a (1) long or (2) malformed header in conjunction with crafted web script.<eos>
# Mitigation Strategies
---

**Vulnerability 1: Denial of Service through CGI Script Denial of Service**
* Disable the mod_cgid module in Apache HTTP Server.
* Use a web application firewall (WAF) to detect and block CGI script attacks.

**Vulnerability 2: Denial of Service through Mod_Deflate CPU Consumption**
* Upgrade Apache HTTP Server to 2.4.10 or later.
* Disable mod_deflate module in Apache HTTP Server.

**Vulnerability 3: Cross-Site Scripting (XSS) in make_variant_list Function**
* Disable MultiViews option in Apache HTTP Server.
* Use a secure alternative for constructing variant lists, such as using mod_rewrite or mod_proxy.

**Vulnerability 4: Denial of Service through APPFtpHandler**
* Upgrade Apache HTTP Server to 2.0.63 or later.
* Disable the ap_proxy_ftp_handler function in Apache HTTP Server.

**Vulnerability 5: Denial of Service through CRF Injection**
* Use mod_rewrite to rewrite the "Location" header to a valid URL before it is sent to the client.
* Disable the use of mod_userdir in Apache HTTP Server.

**Vulnerability 6: Cross-Site Scripting (XSS) in balancer_handler Function**
* Use a secure alternative for constructing balancer URLs, such as using mod_rewrite.
* Disable the use of third-party modules outside of the authentication phase in Apache HTTP Server.

**Vulnerability 7: Cross-Site Scripting (XSS) in dav_xml_get_cdata Function**
* Use a secure alternative for handling CDATA sections, such as using mod_security.
* Upgrade Apache HTTP Server to 2.4.8 or later.

**Vulnerability 8: Cross-Site Scripting (XSS) in balancer_handler Function**
* Use a secure alternative for constructing balancer URLs, such as using mod_rewrite.
* Disable the use of third-party modules outside of the authentication phase in Apache HTTP Server.

**Vulnerability 9: Denial of Service through Scoreboard Attack**
* Disable the use of the scoreboard module in Apache HTTP Server.
* Use a secure alternative for managing server settings, such as using mod_config.

**Vulnerability 10: Denial of Service through Log Cookie Attack**
* Use a secure alternative for handling cookies, such as using mod_security.
* Disable the use of log_cookie in Apache HTTP Server.<eos>
# Penetration testing for 10.10.0.14

## Port 21
### Vulnerabilities that we exploited to get a shell
This module exploits a malicious backdoor that was added to the VSFTPD download archive. This backdoor was introduced into the vsftpd-2.3.4.tar.gz archive between June 30th 2011 and July 1st 2011 according to the most recent information available. This backdoor was removed on July 3rd 2011.

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


### Potential Impacts
- Exploitation of the backdoor could allow an attacker to gain unauthorized access to the system.
- Exploitation of the backdoor could allow an attacker to execute malicious code on the system.
- Exploitation of the backdoor could allow an attacker to gain access to sensitive data.
- Exploitation of the backdoor could allow an attacker to disrupt system operations.
### Mitigation Strategies
**Vulnerability 1:** Malicious Backdoor in VSFTPD Download Archive

* **Patch:** Upgrade to VSFTPD version 2.3.5 or later.
* **Monitor:** Check for updates to VSFTPD regularly.
* **Disable:** Disable the use of the backdoor by setting the `vsftpd_enable_backdoor` environment variable to `false`.

**Vulnerability 2:** Lack of Regular Security Updates

* **Patch:** Install security updates for the operating system and all software applications.
* **Monitor:** Set up automatic security updates to ensure timely patching.
* **Use:** Use a security scanner to identify and remediate vulnerabilities in the system.

**Vulnerability 3:** Insufficient Logging and Monitoring

* **Log:** Enable logging for critical security events.
* **Monitor:** Monitor logs for suspicious activity and system errors.
* **Alert:** Set up alerts for critical security events.
## Port 23
### Vulnerabilities that we are unable to exploit
The HTTP server in AsusWRT has a flaw where it allows an unauthenticated client to perform a POST in certain cases. This can be combined with another vulnerability in the VPN configuration upload routine that sets NVRAM configuration variables directly from the POST request to enable a special command mode. This command mode can then be abused by sending a UDP packet to infosvr, which is running on port UDP 9999 to directly execute commands as root. This exploit leverages that to start telnetd in a random port, and then connects to it. It has been tested with the RT-AC68U running AsusWRT Version 3.0.0.4.380.7743.

| Exploit Name | exploit/linux/http/asuswrt_lan_rce |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 23 |
| UserAgent | Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15 |
| DigestAuthIIS | True |
| SSLVersion | Auto |
| FingerprintCheck | True |
| DOMAIN | WORKSTATION |
| HttpTraceColors | red/blu |
| HTTP::uri_encode_mode | hex-normal |
| HTTP::pad_method_uri_count | 1 |
| HTTP::pad_uri_version_count | 1 |
| HTTP::pad_method_uri_type | space |
| HTTP::pad_uri_version_type | space |
| HTTP::pad_get_params_count | 16 |
| HTTP::pad_post_params_count | 16 |
| CPORT | 41499 |
| CHOST | 10.10.0.13 |
| ASUSWRTPORT | 80 |

| Payload Name | cmd/unix/interact |
| --- | --- |
| Payload Description | Interacts with a shell on an established socket connection |
| CreateSession | True |
| AutoVerifySession | True |


### Potential Impacts
- Unauthenticated client can perform a POST in certain cases.
- NVRAM configuration variables can be set directly from the POST request.
- Special command mode can be abused by sending a UDP packet to infosvr.
- Telnetd can be started in a random port and connected to.
### Mitigation Strategies
**Vulnerability 1: POST Request Flaw**
- Implement input validation to ensure the client sends a proper POST request.
- Use a library or extension to validate the POST request body.
- Use a firewall to block any unauthorized POST requests.

**Vulnerability 2: VPN Configuration Upload**
- Use a secure configuration management tool to manage VPN configuration.
- Use a VPN server with strong authentication and access control.
- Use a VPN client with a built-in vulnerability scanner.

**Vulnerability 3: UDP Packet Exploitation**
- Use a firewall to block any UDP traffic on port UDP 9999.
- Use a VPN server with strong authentication and access control.
- Use a VPN client with a built-in vulnerability scanner.
## Port 2121
### Vulnerabilities that we are unable to exploit
This module abuses a command injection vulnerability in the Nagios3 history.cgi script.

| Exploit Name | exploit/unix/webapp/nagios3_history_cgi |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 2121 |
| UserAgent | Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15 |
| DigestAuthIIS | True |
| SSLVersion | Auto |
| FingerprintCheck | True |
| DOMAIN | WORKSTATION |
| HttpTraceColors | red/blu |
| HTTP::uri_encode_mode | hex-normal |
| HTTP::pad_method_uri_count | 1 |
| HTTP::pad_uri_version_count | 1 |
| HTTP::pad_method_uri_type | space |
| HTTP::pad_uri_version_type | space |
| HTTP::pad_get_params_count | 16 |
| HTTP::pad_post_params_count | 16 |
| TARGETURI | /nagios3/cgi-bin/history.cgi |
| USER | nagiosadmin |
| PASS | nagiosadmin |

| Payload Name | cmd/unix/bind_aws_instance_connect |
| --- | --- |
| Payload Description | Creates an SSH shell using AWS Instance Connect |
| REGION | us-east-1 |
| CreateSession | True |
| AutoVerifySession | True |


### Potential Impacts
- Malicious scripts can be executed on the server.
- Sensitive information, such as passwords and credit card numbers, can be leaked.
- The server can be compromised and used for malicious purposes.
- The Nagios3 system can be taken down.
- The Nagios3 system can be used to spy on or monitor users.
### Mitigation Strategies
---

**Vulnerability 1: Command Injection**

* **Patch the vulnerable script:** Update Nagios3 to version 3.6.0 or later.
* **Use a prepared statement:** Use prepared statements to execute queries, preventing SQL injection attacks.
* **Use a library:** Use a library like `pymysql` to execute queries securely.

**Vulnerability 2: Cross-Site Scripting (XSS)**

* **Validate user input:** Always validate user input before using it in any context.
* **Use a library:** Use a library like `bleach` to escape user input before using it.
* **Use a Sanitizer:** Use a sanitizer like `bleach` to escape user input before using it.

**Vulnerability 3: Out-of-Memory (OOM)**

* **Use a memory-safe data structure:** Use a memory-safe data structure like `collections.deque` to store data.
* **Implement a garbage collector:** Implement a garbage collector to automatically clean up unused objects.
* **Use a profiling tool:** Use a profiling tool to identify and fix memory leaks.
## Port 3306
### Vulnerabilities that we are unable to exploit
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

Multiple buffer overflows in yaSSL 1.7.5 and earlier, as used in MySQL and possibly other products, allow remote attackers to execute arbitrary code via (1) the ProcessOldClientHello function in handshake.cpp or (2) "input_buffer& operator>>" in yassl_imp.cpp.

* Its CVE number is CVE-2008-0226.
* Its CVSS score is 7.5.
* Its CVSS vector is AV:N/AC:L/Au:N/C:P/I:P/A:P

| Exploit Name | exploit/linux/mysql/mysql_yassl_hello |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 3306 |
| SSLVersion | Auto |
| SSLVerifyMode | PEER |
| CPORT | 55007 |
| CHOST | 10.10.0.13 |
| ConnectTimeout | 10 |

| Payload Name | generic/custom |
| --- | --- |
| Payload Description | Use custom string or file as payload. Set either PAYLOADFILE or PAYLOADSTR. |


### Potential Impacts
- Remote attackers can execute arbitrary code.
- Remote attackers can cause a denial of service (memory corruption and daemon crash).
### Mitigation Strategies
**Vulnerability 1: Multiple stack-based buffer overflows in the CertDecoder::GetName function in src/asn.cpp in TaoCrypt in yaSSL before 1.9.9**

* Update the `GetName` function to use a size-constrained buffer for the name field.
* Validate the length of the name field before using it.
* Use a library function to perform the string manipulation.

**Vulnerability 2: Multiple buffer overflows in yaSSL 1.7.5 and earlier**

* Use a size-constrained buffer for the input buffer.
* Validate the length of the input buffer before using it.
* Use a library function to perform the string manipulation.
## Port 5432
### Vulnerabilities that we are unable to exploit
This module can be used to install a WAR file payload on JBoss servers that have an exposed "jmx-console" application. The payload is put on the server by using the jboss.system:BSHDeployer\'s createScriptDeployment() method.

| Exploit Name | exploit/multi/http/jboss_bshdeployer |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 5432 |
| UserAgent | Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15 |
| DigestAuthIIS | True |
| SSLVersion | Auto |
| FingerprintCheck | True |
| DOMAIN | WORKSTATION |
| HttpTraceColors | red/blu |
| HTTP::uri_encode_mode | hex-normal |
| HTTP::pad_method_uri_count | 1 |
| HTTP::pad_uri_version_count | 1 |
| HTTP::pad_method_uri_type | space |
| HTTP::pad_uri_version_type | space |
| HTTP::pad_get_params_count | 16 |
| HTTP::pad_post_params_count | 16 |
| TARGETURI | /jmx-console |
| VERB | POST |

| Payload Name | cmd/unix/bind_aws_instance_connect |
| --- | --- |
| Payload Description | Creates an SSH shell using AWS Instance Connect |
| REGION | us-east-1 |
| CreateSession | True |
| AutoVerifySession | True |


### Potential Impacts
- **Uncontrolled Code Execution:** The WAR file payload can be executed on the server, potentially leading to malicious code execution.
- **Denial-of-Service:** The server may be unable to handle the increased load from the payload, leading to a denial-of-service attack.
- **Data Breaches:** The payload can be used to access sensitive data on the server, such as passwords or credit card information.
- **Remote Code Execution:** The payload can be used to execute code on the server, potentially giving attackers full control of the system.
### Mitigation Strategies
---
**Vulnerability 1: Unrestricted File Upload**
* Use a whitelist of allowed file extensions for deployment scripts.
* Implement file size limits.
* Use a library like Apache Commons FileUpload to handle file uploads.

**Vulnerability 2: Injection**
* Sanitize all user-supplied input before using it in any context.
* Use prepared statements for database queries.
* Use a library like Apache Commons JDBC to handle database operations.

**Vulnerability 3: Cross-Site Scripting (XSS)**
* Sanitize all user-supplied input before using it in any context.
* Use a library like Apache Commons Text to handle HTML content.
* Use a web application firewall (WAF) to protect against XSS attacks.

**Vulnerability 4: Out-of-Memory (OOM) Attack**
* Use a memory-efficient algorithm for data processing.
* Implement a garbage collection mechanism.
* Use a library like Apache Commons Collections to handle collections efficiently.

**Vulnerability 5: Security Misconfiguration**
* Review and configure security settings on JBoss servers.
* Use a vulnerability scanner to identify and remediate security vulnerabilities.
* Implement a security information and event management (SIEM) solution to monitor and analyze security events.
## Port 5900
### Vulnerabilities that we are unable to exploit
This module exploits a command injection vulnerability in IGEL OS Secure Terminal and Secure Shadow services. Both Secure Terminal (telnet_ssl_connector - 30022/tcp) and Secure Shadow (vnc_ssl_connector - 5900/tcp) services are vulnerable.

| Exploit Name | exploit/linux/misc/igel_command_injection |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 5900 |
| CPORT | 52215 |
| CHOST | 10.10.0.13 |
| SSL | True |
| SSLVersion | Auto |
| SSLVerifyMode | PEER |
| ConnectTimeout | 10 |
| SRVHOST | 0.0.0.0 |
| SRVPORT | 8080 |
| HTTP::compression | none |
| HTTP::server_name | Apache |
| CMDSTAGER::FLAVOR | auto |
| AutoCheck | True |

| Payload Name | generic/custom |
| --- | --- |
| Payload Description | Use custom string or file as payload. Set either PAYLOADFILE or PAYLOADSTR. |


### Potential Impacts
- Remote code execution
- Accessing sensitive information
- Taking control of the system
- Disrupting network traffic
- Exposing sensitive data
- Compromising the system's integrity
### Mitigation Strategies
---
**Vulnerability 1: Command Injection in IGEL OS Secure Terminal and Secure Shadow Services**

* **Disable Telnet and VNC access by default.**
* **Use strong passwords for all remote access credentials.**
* **Implement input validation and output sanitization on all remote commands.**
* **Use a firewall to block all unauthorized access ports.**
* **Implement a vulnerability scanner to identify and patch known vulnerabilities.**

**Vulnerability 2: Command Injection in vnc_ssl_connector**

* **Disable vnc_ssl_connector service.**
* **Use a firewall to block all unauthorized access ports.**
* **Implement input validation and output sanitization on all vnc_ssl_connector inputs.**
* **Use a vulnerability scanner to identify and patch known vulnerabilities.**
## Port 6667
### Vulnerabilities that we are unable to exploit
This module exploits a malicious backdoor that was added to the Unreal IRCD 3.2.8.1 download archive. This backdoor was present in the Unreal3.2.8.1.tar.gz archive between November 2009 and June 12th 2010.

| Exploit Name | exploit/unix/irc/unreal_ircd_3281_backdoor |
| --- | --- |
| WfsDelay | 2 |
| RHOSTS | 10.10.0.14 |
| RPORT | 6667 |
| SSLVersion | Auto |
| SSLVerifyMode | PEER |
| CPORT | 45663 |
| CHOST | 10.10.0.13 |
| ConnectTimeout | 10 |

| Payload Name | cmd/unix/adduser |
| --- | --- |
| Payload Description | Creates a new user. By default the new user is set with sudo but other options exist to make the new user automatically root but this is not automatically set since the new user will be treated as root (and login may be difficult). The new user can also be set as just a standard user if desired. |
| CreateSession | True |
| AutoVerifySession | True |
| USER | metasploit |
| PASS | Metasploit$1 |
| RootMethod | SUDO |
| CheckSudoers | True |


### Potential Impacts
- Exploitation of the backdoor could allow malicious actors to gain access to the system, install malware, or launch other attacks.
- Exploitation of the backdoor could also allow malicious actors to steal sensitive information, such as passwords, credit card numbers, or other sensitive data.
- Exploitation of the backdoor could also allow malicious actors to gain control of the system and make it do their bidding.
### Mitigation Strategies
**Vulnerability 1:** Malicious Backdoor in Unreal IRCD 3.2.8.1 Download Archive

* **Update Unreal Engine to 4.27 or later.** This version of the engine does not contain the malicious backdoor.
* **Disable all third-party plugins and mods.** Third-party plugins and mods can sometimes contain malicious code that can exploit vulnerabilities.
* **Use a trusted antivirus program.** Antivirus programs can help to scan for and block malicious code.
* **Do not download files from untrusted sources.** Only download files from official sources.

**Vulnerability 2:** Malicious Backdoor in Unreal3.2.8.1.tar.gz Archive

* **Do not extract the archive.** Extracting the archive can introduce malicious code into your system.
* **Use a reputable antivirus program.** Antivirus programs can help to scan for and block malicious code.
* **Scan your system for malware.** Malware can be installed through phishing emails or other malicious links.
* **Keep your operating system and software up to date.** This will help to patch any known vulnerabilities.

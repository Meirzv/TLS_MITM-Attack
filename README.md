# TLS_MITM-Attack
SSL Strip attack


Explanation About the sslstrip Attack:
A sslstrip attack is a man in the middle (MITM) attack that takes advantage of the transition from HTTP pages to HTTPS pages. In order to have a successful attack, which would mean preventing the client from starting an HTTPS connection with the server, the sslstrip attack will create 2 connections:
1.	 From the client to the MITM
a.	Instead of creating an HTTPS connection with the server, the client starts an unsecured HTTP connection with the MITM.
b.	A secured connection between the client and MITM can be established (HTTPS), but the client will be redirected to a different domain (PayPaI.com instead of PayPal.com). This happens because the attacker needs to get a certificated domain, which is very easy today to do. For example, letsencrypt.com is a free service for this. This secured connection might help to gain the victim’s trust.
2.	From the MITM to the server – The MITM and the server will establish an HTTPS connection. The connection will be a regular client-server connection and the server will not suspect anything.
In addition to the above, the sslstrip has some extra functions to gain the victim’s trust with the HTTP connection, like replacing favicon.ico to a lock icon, and terminating session cookies after 5 minutes.

Explanation About HTTP Strict Transport Security (HSTS):
HSTS is a header in the HTTP response. The goal of this header is to secure websites against eavesdropping (in this lab sslstrip) by connecting clients to servers in a secure way (HTTPS) as early as possible in the connection phase. The steps are:
1.	A client sends a HTTP request (unsecured) to a server http://www.meir.com. 
2.	The server, wanting to create a SSL (TLS) connection, redirects the client with 307 HSTS Policy (HTTP 302 also) to the secured website. 
3.	When the connection is secured (HTTPS) the server will send a HTTP Strict Transport Security header (i.e. Strict-Transport-Security: max-age=31536000;) to the client to be cached.
When a client completes these steps, the HSTS header is cached in the browser. Therefore, the next HTTP request that the client will send to the same server will be a HTTPS request. In addition, there is a possible limitation in this process. For example, if an attacker intercepts the HSTS header, the client will not process the HSTS header and will not send a new HTTPS request to the server. In this case, a sslstrip attack can be useful because the client did not initiate a secured connection.

Today, there are tools that try to enforce the use of HSTS. For example, in order to find a new website and see the behavior of HSTS, I looked for a website that is not cached in my browser (cached websites will choose HTTPS automatically). I searched on Google for a bank website, and HSTS was built into every link that I got from Google (potential victim). Also, there are many preloaded domains. If the domain is preloaded, then browsing to this domain will automaticity use HTTPS. Every domain owner can add his domain to the preloaded list on following website https://hstspreload.org. 

In the example below, which I captured with Safari developer tools, the referrer website was HTTP (in bold). This happens when the client browses to a HTTP request and gets HTTP status code 307, which redirects the client to the HTTPS page. Also, the HSTS header is in the HTTPS response from the server. However, browsing the internet with the developer tools option open showed me that even though websites redirect clients to HTTPS, these website do not necessarily use the HSTS header, which leaves them vulnerable to sslstrip attacks.   

Example for HTTPS packet with HSTS header:

Summary
URL: https://mfa.gov.il/MFA/Pages/default.aspx
Status: 200 OK
Source: Network
Address: 127.0.0.1:43891

Request
GET /MFA/Pages/default.aspx HTTP/1.1
Cookie: BotMitigationCookie_7831042359708280488="883449001551129744bwYb9vZelf2CVI/kFNd9TGuMkNc="
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Cache-Control: max-age=0
Referer: http://mfa.gov.il/
Upgrade-Insecure-Requests: 1
Host: mfa.gov.il
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: keep-alive

Response
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: ASP.NET_SessionId=v04udf55egqassvizpobbl45; path=/; HttpOnly
X-XSS-Protection: 1; mode=block
Expires: Sun, 10 Feb 2019 22:10:07 GMT
Vary: Accept-Encoding
Cache-Control: private, max-age=0
Date: Mon, 25 Feb 2019 22:10:22 GMT
Content-Length: 939420
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Last-Modified: Mon, 25 Feb 2019 22:10:07 GMT
X-MS-InvokeApp: 1; RequireReadOnly
SPRequestGuid: c4b41547-e66d-451f-95ca-0cba7db7b9b9
X-Adguard-Filtered: Adguard for Mac; version=1.5.14
X-AspNet-Version: 2.0.50727
Server
s: 1
Strict-Transport-Security: max-age=31536000; preload
X-SharePointHealthScore: 0



In order to be the MITM, I wrote a Python script using Scapy to initiate an ARP poising attack. ARP is a protocol that translates IP addresses to MAC addresses and vice versa. The ARP poisoning attack happens in the data link layer, when the victim machine is misled to think that the switch is the MITM (Kali Linux), and the router is misled to think that the victim machine is MITM, as shown in the next picture, where the earth symbol is the router, the MITM is Kali Linux, and the victim is Windows XP

The ARP poisoning attack steps:
1.	The MITM sends a custom ARP reply packet to Windows XP, which is identified as the ext-rtr with the IP 10.10.111.1 and MAC address belonging to Kali linux 00:00:00:00:00:04.
2.	The MITM sends a custom ARP reply packet to ext-rtr, which is identified as Windows XP with the IP 10.10.111.108 and MAC addresses belonging to Kali linux 00:00:00:00:00:04.

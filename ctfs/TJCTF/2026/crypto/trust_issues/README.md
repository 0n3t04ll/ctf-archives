thegreenmallard
I made my own DNS resolver and I made sure I could trust it as much as my nameserver by using an even bigger elliptic curve

The admin bot will visit trust-issues.tjc.tf by querying the DNS resolver (which will be instanced), and the DNS resolver will query the nameserver to find the ip address of the website

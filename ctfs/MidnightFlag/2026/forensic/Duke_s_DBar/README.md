WannaCry

A serial killer doesn't just take lives — he takes identities.
In every case, investigators find the same afterimage: the victim's accounts are briefly used to access their own infrastructure, as if the killer wanted someone to watch what he did next. Then everything goes quiet again.

Last night, a Grafana monitoring instance tied to a victim's environment was exposed to the Internet for a short window. During that time, a local file was exfiltrated using a recent vulnerability.

You recovered only two artifacts from the incident window:

Provided artifacts

grafana.log
grafana.db
The attacker blended into background monitoring activity and Internet noise. Your task is to isolate the malicious actions and reconstruct the truth.

Objectives
Find:

The CVE identifier of the vulnerability used.
The full path of the exfiltrated file.
The attacker's source IP address.
The Grafana username (login) that carried out the malicious actions.
Flag format
MCTF{CVE-XXXX-XXXXX:path:ip:username}

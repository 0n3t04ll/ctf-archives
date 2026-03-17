Anh4ckin

Friday the 13th, 23:59. The Executioner has fully compromised the city’s Active Directory domain.

At exactly 23:59, we detected a DCSync operation initiated from a Tier 0 account, targeting the Domain Controller and extracting critical secrets. We have recovered only one artifact from the incident. Your task is to analyze it to reconstruct the initial access before the DCSync and uncover the truth before dawn.

From this artifact, you must identify:

The attacker’s IP address
The SID of the compromised account
The name of the compromised account
The password of the compromised account
The name of the attack used to compromise the account
Flag Format : echo "127.0.0.1:SID;toto;passwd;Attaquename" | sha256sum MCTF{sha256hash}

A developer is experimenting with a counter‑less, merit‑based authentication methods.

Level 1 is their first attempt.

Application AID
A0000000624857494F4348414C4C

SELECT LEVEL
Use this command to select a level.

Note: Selecting the same level twice has no effect (it does not reset the authentication state).

Field	Value	Description
CLA	08
INS	01
P1	XX	Level selector (see below)
P2	00
Possible P1 values
Level	P1	Description
1:LEVEL_BRUTE_FORCE	1	Brute force level
2:LEVEL_TEAR_IN_LOOP	2	Tear within a loop
3:LEVEL_TEAR_AT_INDEX	3	Tear at a specific index
GET STATUS
Field	Value	Description
CLA	08
INS	57
P1	00
P2	00
The returned value represents the card state:

1st byte: 00 if not authenticated, 01 if authenticated.
2nd byte: The current selected level. 00 if no level is selected.
GET FLAG
Field	Value	Description
CLA	08
INS	42
P1	00
P2	00
You must be authenticated to get the flag!

AUTHENTICATE
Field	Value	Description
CLA	08
INS	20
P1	XX
P2	XX
Use this command to authenticate.

The following values are relevant only for level 1. Possible returned status words:

Incorrect parameters (P1, P2): 0x6A86
Wrong parameter value (P1, P2): 0x6B00
Tools: You can ask us a Proxmark3 RDV4. You can reflash its main firmware if needed but NEVER reflash the BOOTROM!! And firstly, make sure ModemManager is NOT running on your Linux.

The code repository and documentation are on https://github.com/RfidResearchGroup/proxmark3.

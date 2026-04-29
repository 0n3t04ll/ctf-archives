greyroad__
Case brief On February 3, 2026, a confidential tip reached your desk. "Hades Market", a pseudonymous prediction-market venue listing contracts on real-world outcomes involving journalists, streamers, and political activists, had been traced to a private Telegram channel operating as "Hades Group." The market was the front: traders took positions on whether specific individuals would be doxxed, swatted, or exposed by specific dates. The Telegram group was the back: a coordination room where the operator brokered the services that settled those contracts (doxxed profiles, coordinated swatting planning, brokered access to private records), so that their own book cleared in their favor. A source obtained a full export of the group's message history before being removed. The export covers roughly six weeks of activity across about 25 accounts, a mix of regular participants, one-time visitors, and apparent administrators. It is attached as hadesexport.json. You have been engaged as the independent OSINT investigator.

Your objective Identify the group owner: the individual operating the service, the one clearing the spread on every contract Hades Market settled. The owner never posts under a personal account; all their messages appear as anonymous group posts (fromid beginning with "channel"). They are not perfectly silent, however.

Flag Submit UMDCTF{REC-XXXXXXX}, where REC-XXXXXXX is the Document Record ID returned by the final document bot at the end of the owner's investigative chain.

Investigative assets

Rules

Do not flood the bots with automated requests.
The bots only return data on seeded targets. Do not use them against real Telegram accounts or usernames outside the export. If a fictional handle in the export happens to collide with a real account, ignore the real account entirely.
You are only permitted to use the provided JSON export and the bots listed above. No external scraping, no queries against live Telegram profiles, nothing beyond this kit.
Do not share the flag, Record IDs, specific methodology, bot handles, or export data publicly while the CTF is running.
Technical issues If a bot doesn't respond, returns something that looks broken, or you hit a problem with the export file itself, open a ticket in the UMDCTF Discord with the bot handle, the query you sent, and what you got back (or didn't).

Fine print All personas, records, and identifiers in this challenge are fictional and generated for CTF use.

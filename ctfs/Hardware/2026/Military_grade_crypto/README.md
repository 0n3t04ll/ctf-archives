Our access control system implements the best of the best!

It accepts only MIFARE Ultralight AES cards
Cards keys are diversified with a secure CMAC-based KDF as defined in AN10922
Reader nonces are generated with an ADC-based TRNG
Level 3: You have to present another card with another UID and perform a valid mutual authentication with the reader to get your flag. All our cards are known to the reader so you've to forge yours.

Ultralight AES docs: https://www.nxp.com/products/MF0AESx20

For RFID challenges, ask us a Proxmark3 RDV4. You can reflash its main firmware if needed but NEVER reflash the BOOTROM!! And firstly, make sure ModemManager is NOT running on your Linux.

The code repository and documentation are on https://github.com/RfidResearchGroup/proxmark3.

PLEASE DON'T ATTEMPT TO OPEN THE BOX! This is an RFID challenge, not an anti-tampering challenge ;)

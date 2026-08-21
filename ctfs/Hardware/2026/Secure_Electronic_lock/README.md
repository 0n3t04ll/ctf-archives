HWCTF designs and sells smart electronic locks that use electronic keys that cannot be counterfeit thanks to a security chip that is embedded in the key itself. Their user manual describes how the system works:

Our keys are electronically safe and secure: they are one-time programmable and contains a hardware unique 32-bit identifier set in factory. This identifier is used within our smartlock control software to enroll and remove keys from authorized lists as well as setting access restrictions based on a specific schedule or time period.

Thanks to HWCTF's strong authentication mechanism, our locks thoroughly check each key's cryptographic signature using our own 256-bit encryption key.

Will you be able to find a vulnerability in their smart lock solution and force one of their locks to open by simply using a key that is not allowed ? To help you a bit in this task, we already made a capture of a communication between a lock and a valid key, cf attached file.

Important note: our locks are sealed and should not be opened, any suspicious validation will be investigated and could lead to a ban if we found out a team has cheated.

`The following hardware and gear is available at our desk:

a binocular with dedicated tools for micro-soldering (soldering iron, solder, tweezers, flux, soldering wick, enameled copper wire, ...)
2.54mm pin headers
breadboards with Dupont wires for prototyping
soldering irons with .5mm solder spool
a wide range of MCUs if needed: RPi Pico 2, Waveshare RP2040, Arduino Nanos, some ESP32s
CD74HS4067 modules (analog multiplexers)
various resistors and capacitors
logic analyzers
FTDI adapters
Remember, you can borrow stuff but have to give it back once the challenge completed or the CTF over.

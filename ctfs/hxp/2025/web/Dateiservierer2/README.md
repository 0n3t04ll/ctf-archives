by 0xbb
web misc

Description:
Herr Ober bitte servieren Sie mir die Dateien nocheinmal.

Use the flag for Dateiservierer as the decryption key for the download:

echo -n 'hxp{the_flag}' | openssl aes-256-cbc -pbkdf2 -iter 100000 -salt -d -pass stdin -in Dateiservierer2.tar.xz.enc -out Dateiservierer2.tar.xz

by katharina and hlt

Description:
🤡 dev for 🤡 software

Use the flag for orakel-von-hxp as the decryption key for the download:

echo -n 'hxp{the_flag}' | openssl aes-256-cbc -pbkdf2 -iter 100000 -salt -d -pass stdin -in cassandra-von-hxp.tar.xz.enc -out cassandra-von-hxp.tar.xz

Hint: The flag is continously input on UART1.

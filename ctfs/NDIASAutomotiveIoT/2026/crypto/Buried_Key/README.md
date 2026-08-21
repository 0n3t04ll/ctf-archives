hard rev crypto
English
A binary performs AES-128-based whitebox encryption. Extract the key and decrypt the following ciphertext using AES-128-ECB with PKCS#7 padding.

Ciphertext: ba720d90a039d801adf22f86d2901b918f36fbbfa6459accb1c5315d1bd4cb39

Note: The binary's output does not match standard AES-128 due to an internal transformation.

日本語
あるバイナリが AES-128 ベースのホワイトボックス暗号化を行っている。 鍵を取り出して、以下の暗号文を AES-128-ECB（PKCS#7 パディング）で復号せよ。

暗号文: ba720d90a039d801adf22f86d2901b918f36fbbfa6459accb1c5315d1bd4cb39

注意: バイナリの出力は内部変換により通常の AES-128 とは一致しません。

Usage / 使い方
$ ./buried_key <32 hex chars (16-byte plaintext)>
$ ./buried_key 00000000000000000000000000000000
88f98d5e605eac3ee60fb40913896498

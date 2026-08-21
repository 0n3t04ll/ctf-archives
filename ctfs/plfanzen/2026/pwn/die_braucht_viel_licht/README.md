pnw
msic
Author: SeTcbPrivilege

some platns need a lot of light, so they will grow best near widnows.

I have built a fun little driver that shows you information about files in Windows. Perhaps it can also show you the flag?

Connect to the remote instance using SSH. You get access to an interactive shell on a Windows Server 2025 Core installation with the driver installed and running. You can use SFTP to upload files to the machine as well.

The flag is stored in raw ASCII Text on the disk device "\?\PhysicalDrive1". There is no filesystem, the first physical sector contains the flag. You need to escalate privileges to be able to read from raw disk devices (must be NT AUTHORITY\SYSTEM or in the Administrators group). For your convenience, there is also a readflag program at C:\Windows\ReadFlag.exe that reads the first sector and writes it to stdout. It does not give you any special privileges, it's just there to pass the correct parameters for opening the physical disk, since that's hard to do from cmd / powershell.

The handout only contains the sources for the driver and ReadFlag. The full VM image and qemu startscript for local testing can be downloaded here. The files are large (14GB), you should look at the driver source first :) In the VM image that you download you can log into the administrator account using the password Password123!, this is disabled on remote.

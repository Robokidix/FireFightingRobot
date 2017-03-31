from gopigo import *
import sys

fwd()
enc_tgt(1,1,18)
time.sleep(.01)
print(enc_read(0))
print(enc_read(1))
while enc_read(1)<18:
	print read_enc_status(),
print(enc_read(0))
print(enc_read(1))


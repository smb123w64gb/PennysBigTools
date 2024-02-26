import struct
import sys
from enum import IntFlag

def u8(file):
    return struct.unpack("B", file.read(1))[0]
 
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
 
def u32(file):
    return struct.unpack("<I", file.read(4))[0]

def s32(file):
    return struct.unpack("<i", file.read(4))[0]

def f32(file):
    return struct.unpack("f", file.read(4))[0]
def vec3(file):
    return struct.unpack("<fff", file.read(12))[0:3]

mdl = open(sys.argv[1], "rb")

mdl.seek(0xC)
vtxCnt = u32(mdl)
facCnt = u32(mdl)
mdl.seek(0x19)
faces = []
for x in range(facCnt):
    faces.append(u16(mdl)+1)
verts = []
for x in range(vtxCnt):
    verts.append(vec3(mdl))
ext_flag = u8(mdl)


mdl.close()

f = open(sys.argv[1] + ".obj", "w")
f.write("o Test\n")
for x in verts:
    f.write(str("v %.6f %.6f %.6f\n"%(x[0],x[1],x[2])))
cur = 0
for x in faces:
    if(cur == 0):
        f.write(str("f"))
    f.write(str(" %i"%x))
    cur += 1
    if(cur == 3):
        f.write(str("\n"))
        cur = 0
f.close()
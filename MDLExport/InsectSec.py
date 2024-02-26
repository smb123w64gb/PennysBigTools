import struct
import sys
from enum import IntFlag, auto

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
def  countSetBits(n):
    count = 0
    while (n):
        count += n & 1
        n >>= 1
    return count

class MDLext(IntFlag):
    TYPE_ONE = auto()
    TYPE_TWO = auto()
    TYPE_THREE = auto()
    TYPE_FOUR = auto()
    

class MDL(object):
    class Extra(object):
        def __init__(self):
            self.type = 0
            self.data = bytes()
        def read(self,f):
            self.type = u16(f)
            size = u32(f)
            self.data = f.read(size)
    def __init__(self):
        self.magic = "MDL\x01"
        self.flags = 0
        self.unk = 0
        self.verts = []
        self.faces = []
        self.frames = 1
        self.roottype = 0
        self.extras = []
    def read(self,f):
        self.magic = f.read(4)
        self.flags = u32(f)
        self.unk = u32(f)
        vertcount = u32(f)
        facecount = u32(f)
        self.frames = u32(f)
        self.roottype = u8(f)
        for x in range(facecount):
            self.faces.append(u16(f))
        for x in range(self.frames):
            vtx = []
            for y in range(vertcount):
                vtx.append(vec3(f))
            self.verts.append(vtx)
        ext_count = countSetBits(self.flags)
        for x in range(ext_count):
            ext = self.Extra()
            ext.read(f)
            self.extras.append(ext)
        




model = open(sys.argv[1], "rb")

mdl = MDL()
mdl.read(model)
model.close()
print(mdl.extras[0].type)

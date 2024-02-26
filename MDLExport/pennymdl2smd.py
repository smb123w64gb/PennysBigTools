import struct
import sys,io
from enum import IntFlag, auto

def u8(file):
    return struct.unpack("B", file.read(1))[0]
 
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def s16(file):
    return struct.unpack("<h", file.read(2))[0]
 
def u32(file):
    return struct.unpack("<I", file.read(4))[0]

def s32(file):
    return struct.unpack("<i", file.read(4))[0]

def f32(file):
    return struct.unpack("f", file.read(4))[0]
def vec3(file):
    return struct.unpack("<fff", file.read(12))[0:3]
def getString(file):
	result = ""
	tmpChar = file.read(1)
	while ord(tmpChar) != 0:
		result += tmpChar.decode("utf-8")
		tmpChar =file.read(1)
	return result
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

class BoneWeghts(object): #0x8
    def __init__(self):
        self.bones = []
        self.weght = []
    def read(self,f,count=1):
        for x in range(count):
            self.bones.append(struct.unpack("<HHHH", f.read(8))[0:4])
            self.weght.append(struct.unpack("BBBB", f.read(4))[0:4])
class Bones(object): #0x7
    def __init__(self):
        self.bonename = []
        self.parrent = []
        self.matrix = []
    def read(self,f):
        for x in range(u16(f)):
            self.bonename.append(getString(f))
            self.parrent.append(s16(f))
            matrixs = []
            for y in range(4):
                mtx = []
                for z in range(4):
                    mtx.append(f32(f))
                matrixs.append(mtx)
            self.matrix.append(matrixs)

class MDL(object):
    class Extra(object):
        def __init__(self):
            self.type = 0
            self.data = bytes()
        def read(self,f):
            self.type = u16(f)
            size = u32(f)
            self.data = f.read(size)
    class BoneWeghts(object): #0x8
        def __init__(self):
            self.bones = []
            self.weght = []
        def read(self,f):
            self.bones = struct.unpack("<HHHH", f.read(8))[0:4]
            self.weght = struct.unpack("BBBB", f.read(4))[0:4]
    class Bones(object): #0x7
        def __init__(self):
            self.bonename = []
            self.parrent = []
            self.matrix = []
        def read(self,f):
            for x in range(u16(f)):
                self.bonename.append(getString(f))
                self.parrent.append(s16(f))
                matrixs = []
                for y in range(4):
                    mtx = []
                    for z in range(4):
                        mtx.append(f32(f))
                    matrixs.append(mtx)
                self.matrix.append(matrixs)
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
for x in mdl.extras:
    if(x.type == 7):
        bonz = Bones()
        bonz.read(io.BytesIO(x.data))
    if(x.type == 8):
        bdata = BoneWeghts()
        bdata.read(io.BytesIO(x.data),len(mdl.verts[0]))
smdout = open(sys.argv[1] + ".smd", "w")
smdout.write("version 1\nnodes\n")
for idx,x in enumerate(bonz.bonename):
    smdout.write("%i \"%s\" %i\n" %(idx,x,bonz.parrent[idx]))
smdout.write("end\nskeleton\ntime 0\n")
for idx,x in enumerate(bonz.matrix):
    smdout.write("%i  %0.6f %0.6f %0.6f  %0.6f %0.6f %0.6f\n"%(idx,x[0][3],x[1][3],x[2][3],0.0,0.0,0.0))
smdout.write("end\ntriangles\n")
fc = 0
for x in mdl.faces:
    if(fc == 0):
        smdout.write("test\n")
    
    smdout.write("0  %.6f %.6f %.6f  %.6f %.6f %.6f  %.6f %.6f" %(mdl.verts[0][x][0],mdl.verts[0][x][1],mdl.verts[0][x][2],0.0,0.0,0.0,0.0,0.0))
    binds = 0
    sr = ""
    for idx,y in enumerate(bdata.weght[x]):
        if(y):
            sr += str(" %i %.6f" % (bdata.bones[x][idx],y/255))
            binds+=1
    smdout.write(" %i%s" % (binds,sr))
    smdout.write("\n")
    fc+=1
    if(fc == 3):
        fc = 0

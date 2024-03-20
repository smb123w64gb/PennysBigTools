#pragma pattern_limit 1000000
struct MDL{
char Magic[4];
u16 meshflags;
u16 vertflags;
u24 blank;
u8 frames;
u32 vertcount;
u32 facecount;
u32 framecount;
u8 pad;
};
struct verts{
float x;
float y;
float z;
};
struct matrix4{
u8 count;
float m0[count];
float m1[count];
float m2[count];
float m3[count];
};
struct sec{
u16 mode;
u32 size;
char data[size];
};

fn countSetBits(u32 n){
    u32 count = 0;
    while (n) {
        count += n & 1;
        n >>= 1;
    }
    return count;
};
MDL hdr @ 0;
u16 faces[hdr.facecount] @ sizeof(hdr);
matrix4 mtx[countSetBits(hdr.vertflags)] @ sizeof(faces) + sizeof(hdr);
verts vtx[hdr.vertcount*hdr.framecount] @ sizeof(faces) + sizeof(hdr) + sizeof(mtx);
sec mode[countSetBits(hdr.meshflags)] @ sizeof(faces) + sizeof(hdr) + sizeof(vtx) + sizeof(mtx);
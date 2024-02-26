#pragma pattern_limit 1000000
struct MDL{
char Magic[4];
u32 flags;
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
verts vtx[hdr.vertcount*hdr.framecount] @ sizeof(faces) + sizeof(hdr);

sec mode[countSetBits(hdr.flags)] @ sizeof(faces) + sizeof(hdr) + sizeof(vtx);
import type.base;

u8 iter_g;

struct RGBA8 {
  u8 red;
  u8 green;
  u8 blue;
  u8 alpha;
} [[static, color(std::format("{:02X}{:02X}{:02X}", red, green, blue))]];

struct GRADIENT{
float pos;
RGBA8 color;
}[[color(color)]];

struct ENT{
u16 grad_count;
GRADIENT grad[grad_count];
};

struct ENT_HDR{
char name[];
ENT entrys[iter_g];
};

struct PAL{
char Magic[4];
u8 iter_gg;
iter_g = iter_gg;
u8 count;
ENT_HDR entrys[count+1];
};

PAL pal @ 0;

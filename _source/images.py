"""Make responsive WebP versions of each photograph. No crop, no filter; ICC kept."""
import sys, os, json
from PIL import Image, ImageOps
src, out = sys.argv[1], sys.argv[2]
MAP = {  # id : source filename
 "s01":"IMG-20260510-WA0037.jpg","s02":"IMG-20260508-WA0024 (1).jpg","s03":"IMG-20260508-WA0026 (1).jpg",
 "s04":"IMG-20260508-WA0015(1) (3).jpg","s05":"IMG-20260510-WA0019(1) (1).jpg","s06":"IMG-20260510-WA0017.jpg",
 "s07":"IMG-20260508-WA0016 (2).jpg","s08":"IMG-20260508-WA0033(1) (4).jpg","s09":"IMG-20260510-WA0022(1).jpg",
 "s10":"IMG-20260510-WA0035.jpg","s11":"IMG-20260508-WA0013 (1).jpg","s12":"IMG-20260523-WA0015 (1).jpg",
 "s13":"IMG-20260510-WA0021(1).jpg","s14":"IMG-20260511-WA0031 (1).jpg","s15":"IMG-20260517-WA0085 (1).jpg",
 "c01":"IMG_0486.JPG","p01":"IMG_3700.JPG","p02":"IMG_3702.JPG","p03":"IMG_3713.JPG","p04":"IMG_3751.JPG",
 "p05":"IMG_3753.JPG","p06":"DSCF4413.JPG",
 "me":"portrait.png"}  # portrait of the photographer, used on Home
WIDTHS=[640,1200,1800]
meta={}
for k,f in MAP.items():
    im=Image.open(os.path.join(src,f)); icc=im.info.get("icc_profile")
    im=ImageOps.exif_transpose(im).convert("RGB")
    w,h=im.size; made=[]
    for tw in WIDTHS:
        if made and made[-1]>=w: break
        tw=min(tw,w); r=im.resize((tw,round(h*tw/w)),Image.LANCZOS)
        kw=dict(quality=84,method=6)
        if icc: kw["icc_profile"]=icc
        r.save(os.path.join(out,f"{k}-{tw}.webp"),"WEBP",**kw); made.append(tw)
    avg=im.resize((1,1),Image.BOX).getpixel((0,0))
    meta[k]={"w":w,"h":h,"widths":made,"color":"#%02x%02x%02x"%avg,"file":f}
json.dump(meta,open(sys.argv[3],"w"),indent=1)
print(json.dumps({k:(v["w"],v["h"],v["widths"]) for k,v in meta.items()}))

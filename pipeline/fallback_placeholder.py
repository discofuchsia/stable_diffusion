from PIL import Image, ImageDraw

def generate_fallback(w:int,h:int,product_name:str,hint:str):
    img=Image.new('RGB',(w,h),(240,240,240)); d=ImageDraw.Draw(img)
    for i in range(0,max(w,h),20):
        shade=200+(i%40); x0,y0=(i,0) if w>=h else (0,i); x1,y1=(i+40,h) if w>=h else (w,i+40)
        d.rectangle([x0,y0,x1,y1], fill=(shade,shade,shade))
    d.rectangle([20,20,min(w-20,420),120], fill=(0,0,0)); d.text((30,50), product_name[:22], fill=(255,255,255))
    if hint: d.text((20,h-40), hint[:48], fill=(80,80,80))
    return img

from PIL import Image
from pyatlas.atlas import Atlas

img = Image.open(r"C:\Users\Admin\NM_TTNT\demo_atlas\map.gif")
#----------------------------------------------------------------------------------------------------------------
# sizes of the map

WIDTH = img.width
HEIGHT = img.height


atlas = Atlas(r"C:\Users\Admin\NM_TTNT\demo_atlas\phuong_thanh_cong.atlas")
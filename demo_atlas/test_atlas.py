from pyatlas.atlas import Atlas

atlas = Atlas('phuong_thanh_cong.atlas')

for node in atlas.nodes():
    print(node)

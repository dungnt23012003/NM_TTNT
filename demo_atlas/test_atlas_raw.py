from pyatlas.atlas import Atlas

atlas = Atlas('VNM_phuong_thanh_cong.osm.atlas')

print(atlas.edges().__next__())

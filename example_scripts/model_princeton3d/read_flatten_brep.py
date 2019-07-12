import os

import shapefile
from py4design import py3dmodel
from py4design import urbangeom

#specify the pt cloud directory
file_dir = "F:\\kianwee_work\\princeton\\2019_06_to_2019_12\\campus_as_a_lab\\model3d\\brep\\main_campus"
filename = "impervious_surface.brep"
result_shp_file = "F:\\kianwee_work\\princeton\\2019_06_to_2019_12\\campus_as_a_lab\\model3d\\shp\\flatten\\flatten_srf_main_campus.shp"
#============================================================================================================
#FUNCTION
#============================================================================================================
def write_poly_shpfile(occface_list, shp_filepath):
    w = shapefile.Writer(shp_filepath, shapeType = 5)
    w.field('index','N',10)
    cnt=0
    for occface in occface_list:
        pyptlist = py3dmodel.fetch.points_frm_occface(occface)
        is_anticlockwise = py3dmodel.calculate.is_anticlockwise(pyptlist, (0,0,1))
        if is_anticlockwise:
            pyptlist.reverse()
        pyptlist2d = []
        for pypt in pyptlist:
            x = pypt[0]
            y = pypt[1]
            pypt2d = [x,y]
            pyptlist2d.append(pypt2d)
        w.poly([pyptlist2d])
        w.record(cnt)
        cnt+=1

#============================================================================================================
#FUNCTION
#============================================================================================================
list_dir = os.listdir(file_dir)
ndir = len(list_dir)
face_list = []
cnt = 0
for dirx in list_dir:    
    print "**********Processing ... ", cnt+1, "/", ndir, "folder", dirx
    folder = os.path.join(file_dir, dirx)
    filepath = os.path.join(file_dir, dirx, filename)
    
    if os.path.isfile(filepath):
        cmpd = py3dmodel.utility.read_brep(filepath)
        
        #==================================================================
        #ACTIVATE THIS IF IT IS A BUILDIN FILE
        #==================================================================
#        solids = py3dmodel.fetch.topo_explorer(cmpd, "solid")
#        flist = []
#        for s in solids:    
#            facades, roofs, footprints = urbangeom.identify_building_surfaces(s)
#            flist.extend(footprints)    
#        
#        cmpd = py3dmodel.construct.make_compound(flist)
        #==================================================================
        #ACTIVATE THIS IF IT IS A BUILDIN FILE
        #==================================================================
        
        faces = py3dmodel.construct.simple_mesh(cmpd)
        face_list.extend(faces)
    cnt+=1

write_poly_shpfile(face_list, result_shp_file)
import os
import time
from pyliburo import citygml2eval
from pyliburo import py3dmodel
#================================================================================
#INSTRUCTION: SPECIFY THE CITYGML FILE
#================================================================================
#specify the citygml file
current_path = os.path.dirname(__file__)
parent_path = os.path.abspath(os.path.join(current_path, os.pardir, os.pardir))
for cnt in range(1):
    citygml_filepath = os.path.join(parent_path, "example_files","citygml", "example1.gml" )
    dae_filepath = os.path.join(parent_path, "example_files","dae", "example1_fai.dae" )
    #or just insert a citygml file you would like to analyse here 
    '''citygml_filepath = "C://file2analyse.gml"'''
    #================================================================================
    #INSTRUCTION: SPECIFY THE CITYGML FILE
    #================================================================================
    
    displaylist2 = []
    evaluations = citygml2eval.Evals(citygml_filepath)
    
    time1 = time.clock()
    print "#==================================="
    print "EVALUATING MODEL ... ...", citygml_filepath
    print "#==================================="
    wind_dir = (1,1,0)
    res_dict = evaluations.fai(wind_dir)
    os_cmpd = py3dmodel.construct.make_compound(res_dict["vertical_surface_list"])
    occedge_list = py3dmodel.fetch.topo_explorer(os_cmpd, "edge")
    time2 = time.clock()
    print "TIME TAKEN", (time2-time1)/60

    print "AVERAGE FAI", res_dict["average"]
    d_str = "AVERAGE FAI: " + str(res_dict["average"])
    py3dmodel.export_collada.write_2_collada_falsecolour(res_dict["grids"], res_dict["fai_list"], "FAI", dae_filepath, 
                                                         description_str = d_str, minval = 0.0, maxval = 1.0, 
                                                         other_occedge_list = occedge_list) 
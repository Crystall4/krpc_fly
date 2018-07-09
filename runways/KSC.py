# -*- coding: utf-8 -*-
from runway import *
import sys
sys.path.append("../lib")
sys.path.append("./lib" )
import tools
import handbooks

KSC_West =       coord_from_dict(handbooks.coord.get('KSC_West'))
KSC_East =       coord_from_dict(handbooks.coord.get('KSC_East'))
center_KSP_VPP = KSC_East.target_dot_from_dist_and_bear(KSC_West.bearing_line(KSC_East),(KSC_West.dist_line(KSC_East)/2),name='Center KSC VPP')
KSC_BP   = coordinates(name='Begin Position', lat=-0.04859355505160000, lng=-74.72465205780000000, alt=70.3741567462)

vpp9	 = vpp_bearing(handbooks.KSC9.get('name'), handbooks.KSC9.get('edge1'), handbooks.KSC9.get('edge2'))
vpp27    = vpp_bearing(handbooks.KSC27.get('name'),handbooks.KSC27.get('edge1'),handbooks.KSC27.get('edge2'))

#======================================================================================================================	
#-------------------------------------name----------beg_deg,-end_deg,-STO,--SLA,---centerZ,------subzones-------beg_det----------------------end_det-------------main_route---------------------message------------------------------------------------------------------------------------
KSC_VPP =VPP([vpp9,vpp27],[])
KSC_VPP.zones.append(radialZone("main flight zone 2",   0.0,  45.0,  True,  False, center_KSP_VPP,[12000,24000,32000],[45.0,  666.0, 666.0],[45.0,  666.0, 666.0],[45,0,  666.0, 666.0], [], "Основная летная зона для направлений на север-северовосток"))
KSC_VPP.zones.append(radialZone("main flight zone 1",  45.0,  85.0,  True,  True,  center_KSP_VPP,[12000,24000,32000],[666.0, 666.0, 666.0],[666.0, 666.0, 666.0],[666.0, 666.0, 666.0], [], "Основная летная зона для направлений на восток-юговосток, так же облет запретных зон icelandVPP и GlissEast"))
KSC_VPP.zones.append(radialZone("GlissEast",           85.0, 105.0,  False, True,  center_KSP_VPP,[12000,24000,32000],[83.0,   83.0,  83.0],[45.0,    0.0, 286.0],[],                    [], "Зона глиссады при заходе на восточный край ВПП-KSC"))
KSC_VPP.zones.append(radialZone("icelandVPP",         105.0, 170.0,  False, False, center_KSP_VPP,[12000,24000,32000],[83.0,   83.0,  83.0],[45.0,    0.0, 286.0],[170.0],               [], "Рабочая зона ВПП на острове разрешены полеты только в экстренных случаях на западный заход островной ВПП"))
KSC_VPP.zones.append(radialZone("KSC"       ,         170.0, 255.0,  False, False, center_KSP_VPP,[12000,24000,32000],[83.0,   83.0,  83.0],[45.0,    0.0, 286.0],[],                    [], "Зона KSC,запрещены все полеты"))
KSC_VPP.zones.append(radialZone("GlissWest",          255.0, 285.0,  False, True,  center_KSP_VPP,[12000,24000,32000],[45.0,    0.0, 286.0],[45.0,    0.0, 286.0],[],                    [], "Зона глиссады при заходе на западный край ВПП-KSC"))
KSC_VPP.zones.append(radialZone("main flight zone 3", 285.0, 360.0,  True,  True,  center_KSP_VPP,[12000,24000,32000],[666.0, 666.0, 666.0],[666.0, 666.0, 666.0],[45.0,    0.0, 666.0], [], "Основная летная зона для направлений на северозапад-запад а так же облет запретных зон GlissWest, WaitingArea,"))

# -*- coding: utf-8 -*-
import runway
import sys
sys.path.append("../lib")
sys.path.append("./lib")
import tools
coordinates = tools.coordinates
radialZone=runway.radialZone

KSC_West    = coordinates(name='runwayWest',  lat=-0.04855056049336841, lng=-74.72449313835466000, alt=70.0 )
KSC_East    = coordinates(name='runwayEast',  lat=-0.05025878770915180, lng=-74.48951284451766242, alt=70.0 )

#======================================================================================================================	
#-------------------------------------name----------beg_deg,-end_deg,-STO,--SLA,---centerZ,------subzones-------beg_det----------------------end_det-------------main_route------------message------------------------------------------------------------------------------------
KSC_VPP =runway.VPP(KSC_West,KSC_East)
KSC_VPP.zones.append(radialZone("main flight zone 2",   0.0,  45.0,  True,  False, KSC_East,[12000,24000,32000],[45.0,  666.0, 666.0],[45.0,  666.0, 666.0],[45,0,  666.0, 666.0], "Основная летная зона для направлений на север-северовосток"))
KSC_VPP.zones.append(radialZone("main flight zone 1",  45.0,  85.0,  True,  True,  KSC_East,[12000,24000,32000],[666.0, 666.0, 666.0],[666.0, 666.0, 666.0],[666.0, 666.0, 666.0], "Основная летная зона для направлений на восток-юговосток, так же облет запретных зон icelandVPP и GlissEast"))
KSC_VPP.zones.append(radialZone("GlissEast",           85.0, 105.0,  False, True,  KSC_East,[12000,24000,32000],[83.0,   83.0,  83.0],[45.0,    0.0, 286.0],[],                    "Зона глиссады при заходе на восточный край ВПП-KSC"))
KSC_VPP.zones.append(radialZone("icelandVPP",         105.0, 170.0,  False, False, KSC_East,[12000,24000,32000],[83.0,   83.0,  83.0],[45.0,    0.0, 286.0],[170.0],               "Рабочая зона ВПП на острове разрешены полеты только в экстренных случаях на западный заход островной ВПП"))
KSC_VPP.zones.append(radialZone("KSC"       ,         170.0, 255.0,  False, False, KSC_East,[12000,24000,32000],[83.0,   83.0,  83.0],[45.0,    0.0, 286.0],[],                    "Зона KSC,запрещены все полеты"))
KSC_VPP.zones.append(radialZone("GlissWest",          255.0, 285.0,  False, True,  KSC_East,[12000,24000,32000],[45.0,    0.0, 286.0],[45.0,    0.0, 286.0],[],                    "Зона глиссады при заходе на западный край ВПП-KSC"))
KSC_VPP.zones.append(radialZone("main flight zone 3", 285.0, 360.0,  True,  True,  KSC_East,[12000,24000,32000],[666.0, 666.0, 666.0],[666.0, 666.0, 666.0],[45.0,    0.0, 666.0], "Основная летная зона для направлений на северозапад-запад а так же облет запретных зон GlissWest, WaitingArea,"))

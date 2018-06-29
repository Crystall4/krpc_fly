# -*- coding: utf-8 -*-

import sys
sys.path.append("./lib")
sys.path.append("./runways")
import tools
import runway
coordinates = tools.coordinates
radialZone=runway.radialZone

icelandEast = coordinates(name='icelandEast', lat=-1.51671773150452880, lng=-71.88368709972201000, alt=135.2)
icelandWest = coordinates(name='icelandWest', lat=-1.51772268480006560, lng=-71.96820722802198000, alt=135.2)
ivpp9	 = runway.vpp_bearing("iceland9" ,icelandWest,icelandEast)

iceland_VPP= runway.VPP([ivpp9],[])

#----------------------------------------name--------------------beg_deg,-end_deg,--STO,-SLA,----centerZ,--------subzones------------------beg_det-------------------end_det--------------main_route----------------------------------message--------------------------------------------------------------------									
iceland_VPP.zones.append(radialZone("iceland_GlissEast"         ,   85.0,   105.0, False,True  ,icelandEast,[12000,24000,32000],      [106.0,106.0,106.0],      [106.0,106.0,106.0],      [],                  [], "Зона глиссады при заходе на восточный край островной ВПП"))
iceland_VPP.zones.append(radialZone("iceland_GlissWest"         ,  255.0,   285.0, False,True  ,icelandWest,[12000,24000,32000,64000],[254.0,254.0,254.0,254.0],[254.0,254.0,254.0,254.0],[],                  [], "Зона глиссады при заходе на западный  край островной ВПП"))
iceland_VPP.zones.append(radialZone("from_KSC"                  ,  285.0,   315.0, False,False ,icelandWest,[12000,24000,32000,64000],[254.0,254.0,254.0,254.0],[254.0,254.0,254.0,254.0],[],                  [], "Зона KSC,запрещены все полеты"))
iceland_VPP.zones.append(radialZone("from_KCS_VPP"              ,  315.0,   360.0, False,False ,icelandWest,[12000,24000,32000],      [106.0,106.0,106.0],      [180.0,106.0,106.0],      [355.0],             [], "Рабочая зона ВПП KSC, разрешены полеты только в экстренных случаях на восточный заход ВПП KSC"))
iceland_VPP.zones.append(radialZone("from_KCS_VPP"              ,    0.0,    85.0, False,False ,icelandEast,[12000,24000,32000],      [106.0,106.0,106.0],      [106.0,106.0,106.0],      [355.0],             [], "Рабочая зона ВПП KSC, разрешены полеты только на восточный заход ВПП KSC"))
iceland_VPP.zones.append(radialZone("iceland_main flight zone 1",  105.0,   190.0, True, True  ,icelandEast,[12000,24000,32000],      [666.0,666.0,666.0],      [666.0,666.0,666.0],      [666.0,666.0,666.0], [], "Основная летная зона для направлений на восток-юговосток, так же облет запретных зон KSC_VPP и GlissEast"))
iceland_VPP.zones.append(radialZone("iceland_main flight zone 2",  170.0,   255.0, True, True  ,icelandWest,[12000,24000,32000],      [666.0,666.0,666.0],      [666.0,666.0,666.0],      [666.0,666.0,666.0], [], "Основная летная зона для направлений на югозапад-юг, так же облет запретных зон KSC и GlissWest"))

import sys
sys.path.append("./lib")
sys.path.append("./runways")
from tools import *
import KSC

#from test2 import *

tp = coordinates(name='recursive_dot', lat=-0.000, lng=12.48951284451766242, alt=1500.0)
vp=KSC.KSC_VPP.get_SID(tp,KSC.KSC_West)
print vp.__str__()





from maya.api.OpenMaya import *

ctrlIK = 'l_arm_ctl_ik'

pV = 'pole_vector_ctl'
# Place ik wrist controler on fk wrist controler
mWristFk = cmds.xform("l_wrist_fk", q=True, matrix=True, ws=True)
cmds.xform(ctrlIK, matrix=mWristFk, ws=True)

#fk position
sFk= MPoint(cmds.xform("l_shoulder_fk", q=True, ws=True, t=True))
eFk= MPoint(cmds.xform("l_elbow_fk", q=True, ws=True, t=True))
wFk= MPoint(cmds.xform("l_wrist_fk", q=True, ws=True, t=True))

# Determine pole vector position 
m= MVector(sFk) + MVector(wFk)
mPrime= m*0.5
mPrimeE = MVector(eFk) - MVector(mPrime)
F= MVector(eFk) + mPrimeE
cmds.xform(pv, t=F, ws=True)





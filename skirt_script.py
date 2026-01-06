import math
import maya.cmds as mc
class eyeTool(object):
    def __init__(self):
        'Constructor'
        def create(type,len):
            start=mc.spaceLocator(n=type+'_start_locator')[0]
            end=mc.spaceLocator(n=type+'_end_locator')[0]
            mc.move(0,1,0,end)
            grp=mc.createNode('transform',n=type+'_group')
            mc.parent(start,grp)
            len=int(len)
            for a in range (1,len):
                dir=str(a)
                r=360.0/len
                mc.rotate(0,r,0,start,r=1)
            
                if not mc.objExists(start+'.angleOut'):
                    mc.addAttr(start,sn='angleOut',k=1)
                    mc.addAttr(start,sn='angleIn',k=1)
                    mc.setAttr(start+'.angleOut',k=0,cb=1)
                    mc.setAttr(start+'.angleIn',k=0,cb=1)
                    mc.setAttr(start+'.angleOut',90)
                jnt_1=mc.joint(start,n=type+'_'+dir+'_base_joint')
                if not mc.objExists(type+'_'+dir+'_skin_joint'):
                    jnt_2=mc.joint(end,n=type+'_'+dir+'_skin_joint')
                mc.parent(type+'_'+dir+'_skin_joint',jnt_1)
                if mc.listRelatives(start,p=1):
                    mc.parent(jnt_1,mc.listRelatives(start,p=1))
                else:
                    mc.parent(jnt_1,w=1)
                dup=mc.duplicate(start,n=start.replace('start',dir+'_dir'))[0]
                mc.setAttr(dup+'.v',0)
                mc.parent(dup,jnt_1)
                mc.setAttr(dup+'.tz',1)
                mc.move(0,0,1,jnt_1,os=1)
                if not mc.listRelatives(jnt_1,p=1):
                    mc.parent(jnt_1,mc.listRelatives(start,p=1))
                mc.parent(dup,grp)
                #
                if not mc.objExists(type+'_base_vector_plusMinusAverage'):
                    pma_1=mc.createNode('plusMinusAverage',n=type+'_base_vector_plusMinusAverage')
                    mc.setAttr(pma_1+'.operation',2)
                    mc.connectAttr(start+'Shape.worldPosition',pma_1+'.input3D[0]')
                    mc.connectAttr(end+'Shape.worldPosition',pma_1+'.input3D[1]')
                
                pma_2=mc.createNode('plusMinusAverage',n=type+'_'+dir+'_plusMinusAverage')
                mc.setAttr(pma_2+'.operation',2)
                mc.connectAttr(start+'Shape.worldPosition',pma_2+'.input3D[0]')
                mc.connectAttr(dup+'Shape.worldPosition',pma_2+'.input3D[1]')
                
                angle=mc.createNode('angleBetween',n=type+'_'+dir+'_angleBetween')
                mc.connectAttr(type+'_base_vector_plusMinusAverage.output3D',angle+'.vector1')
                mc.connectAttr(type+'_'+dir+'_plusMinusAverage.output3D',angle+'.vector2')
                angleValue=mc.getAttr(angle+'.angle')
                setRange=mc.createNode('setRange',n=type+'_'+dir+'_setRange')
                mc.connectAttr(angle+'.angle',setRange+'.valueX')
                mc.connectAttr(angle+'.angle',setRange+'.valueY')
                mc.connectAttr(angle+'.angle',setRange+'.valueZ')
                mc.setAttr(start+'.'+'angleIn',angleValue)
                mc.connectAttr(setRange+'.outValueX',jnt_1+'.rx')
                mc.connectAttr(start+'.'+'angleIn',setRange+'.oldMaxX')
                mc.connectAttr(start+'.'+'angleIn',setRange+'.oldMaxY')
                mc.connectAttr(start+'.'+'angleIn',setRange+'.oldMaxZ')
                
                mc.connectAttr(start+'.'+'angleOut',setRange+'.minX')
                mc.connectAttr(start+'.'+'angleOut',setRange+'.minY')
                mc.connectAttr(start+'.'+'angleOut',setRange+'.minZ')
            mc.parent(end,start)
#windows
        if mc.window("colliderWindow", exists = True):#cheek window
            mc.deleteUI("colliderWindow") 
        self.eyeWindow=mc.window('colliderWindow',t='collider',sizeable=1,mnb=False,mxb=False,w=202,h=62)
        mainCL = mc.columnLayout(w=202,h=62)
        #layout
        rangeBL=mc.gridLayout(parent=mainCL,numberOfColumns=2,cellWidthHeight=(100, 20))
        
        mc.text( label='name' ,h=40)
        name=mc.textField(h=40)
        mc.text( label='len' ,h=40)
        len=mc.textField(h=40)
        
        mc.button(label='build collider',c=lambda x: create(
        mc.textField(name, query = True,text=1),
        mc.textField(len, query = True,text=1)
        ),
        bgc=(1,0.8,0.2))
    def show(self):
        self.show=mc.showWindow(self.eyeWindow)
u=eyeTool()
u.show()






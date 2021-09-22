#****************
#Cantilever Beam Bendng under the uniform pressure load
#
from abaqus import *
from abaqusConstants import *
import regionToolset
session.viewports['Viewport: 1'].setValues(displayedObject=None)

#------------

#Creating Model
mdb.models.changeKey(fromName='Model-1',toName='Cantilever Beam')
beamModel=mdb.models['Cantilever Beam']

#Create Part
import sketch
import part

#1-) sketch the beam crossection using rectangle tool, use mm as dimensions
beamProfileSketch=beamModel.ConstrainedSketch(name='Beam CS Profile',sheetSize=5000)
beamProfileSketch.rectangle(point1=(100,100), point2=(300,-100))
#2-) Creat a 3D deformable part name "Beam", by extrusion
beamPart=beamModel.Part(name='Beam',dimensionality=THREE_D,type=DEFORMABLE_BODY)
beamPart.BaseSolidExtrude(sketch=beamProfileSketch,depth=5000)

#--------------------

#Create Material
import material
beamMaterial=beamModel.Material(name='AISI 1005 Steel')
beamMaterial.Density(table=((7.85E-9, ), ))
beamMaterial.Elastic(table=((200000,0.29), ))
#Create solid section and assign to the beam

import section
beamSection=beamModel.HomogeneousSolidSection(name='Beam Section',material='AISI 1005 Steel')

#Assign to the beam

beam_region=(beamPart.cells,)
beamPart.SectionAssignment(region=beam_region,sectionName='Beam Section')

#Create Assembly
import assembly

#Create the part instance
beamAssembly=beamModel.rootAssembly
beamInstance=beamAssembly.Instance(name='Beam Instance', part=beamPart,dependent=ON)


#Create a Step
import step

#Create a static general step
beamModel.StaticStep(name='Apply Load',previous='Initial',description='Load is appled during this step')


#Create the field output requests
#change the name of field output request 'F-Output-1' to 'Selected Field Outputs'

beamModel.fieldOutputRequests.changeKey(fromName='F-Output-1',toName='Selected Field Outputs')
beamModel.fieldOutputRequests['Selected Field Outputs'].setValues(variables=('S','E','PEMAG','U','RF','CF'))

#Create history output request
beamModel.HistoryOutputRequest(name='Default History Outputs',createStepName='Apply Load',variables=PRESELECT)
#delete the original history output request 'H-Output-1'
del beamModel.historyOutputRequests['H-Output-1']

#Apply Load on the top surface of the beam
top_face_pt_x=200
top_face_pt_y=100
top_face_pt_z=2500
top_face_pt=(top_face_pt_x,top_face_pt_y,top_face_pt_z)
top_face=beamInstance.faces.findAt((top_face_pt,))

#Extract the region of the face choosing which direction its normal points in
top_face_region=regionToolset.Region(side1Faces=top_face)

#Apply pressure load on this region in the 'Apply Load' step
beamModel.Pressure(name='Uniform Applied Pressure',createStepName='Apply Load',region=top_face_region,distributionType=UNIFORM,magnitude=10E-6,amplitude=UNSET)

#Apply ENCASTRE BC
fixed_end_face_pt_x=200
fixed_end_face_pt_y=0
fixed_end_face_pt_z=0
fixed_end_face_pt=(fixed_end_face_pt_x,fixed_end_face_pt_y,fixed_end_face_pt_z)

#the face on which that point lies is the face we are looking for
fixed_end_face=beamInstance.faces.findAt((fixed_end_face_pt,))

#We extract the region of the face choosing which direction its normal points in 
fixed_end_face_region=regionToolset.Region(faces=fixed_end_face)

beamModel.EncastreBC(name='Encastre on end',createStepName='Initial',region=fixed_end_face_region)


#Mesh generation

import mesh
#first we need to locate and select a point inside the solid, place a point somewhere inside it based on our knowledfe of the geometry

beam_inside_xcoord=200
beam_inside_ycoord=0
beam_inside_zcoord=2500
elemType1=mesh.ElemType(elemCode=C3D8,elemLibrary=STANDARD,kinematicSplit=AVERAGE_STRAIN,secondOrderAccuracy=OFF,hourglassControl=DEFAULT,distortionControl=DEFAULT)


beamCells=beamPart.cells
selectedBeamCells=beamCells.findAt((beam_inside_xcoord,beam_inside_ycoord,beam_inside_zcoord),)
beamMeshRegion=(selectedBeamCells,)
beamPart.setElementType(regions=beamMeshRegion,elemTypes=(elemType1,))

beamPart.seedPart(size=100,deviationFactor=0.1)
beamPart.generateMesh()




#---------------------------


#create and run the job

import job
mdb.Job(name='CantileverBeamJob', model='Cantilever Beam', type=ANALYSIS, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, description='Job simulates a loaded cantilever beam', parallelizationMethodExplicit=DOMAIN, multiprocessingMode=DEFAULT, numDomains=1, userSubroutine='', numCpus=1, memory=50, memoryUnits=PERCENTAGE, scratch='', echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF)

#Run the job
mdb.jobs['CantileverBeamJob'].submit(consistencyChecking=OFF)

#Do not return control till the job finihes running

mdb.jobs['CantileverBeamJob'].waitForCompletion()

#Finilization

#post process
import visualization

beam_viewport=session.Viewport(name='BeamResults Viewport')
beam_Odb_Path='CantileverBeamJob.odb'
an_odb_object=session.openOdb(name=beam_Odb_Path)
beam_viewport.setValues(displayedObject=an_odb_object)
beam_viewport.odbDisplay.display.setValues(plotState=(DEFORMED,))




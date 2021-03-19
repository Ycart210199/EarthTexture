#!/usr/bin/env python
 
##
# This example shows how to apply an vtkImageData texture to an sphere 
# vtkPolyData object.
# Note: Input jpg file can be located in the VTKData repository.
#
# @author JBallesteros
##
 
import vtk

jpegfile = "Earth3.jpg"
#jpegfile = "eye3.jpg"

class vtkTimerCallback():
    def __init__(self, steps, actor, iren):
        self.timer_count = 0
        self.steps = steps
        self.actor = actor
        self.iren = iren
        self.timerId = None

    def execute(self, obj, event):
        step = 0
        while step < self.steps:
            print(self.timer_count)
            self.actor.SetPosition(self.timer_count / 100.0, self.timer_count / 100.0, 0)
            iren = obj
            iren.GetRenderWindow().Render()
            self.timer_count += 1
            step += 1
        if self.timerId:
            iren.DestroyTimer(self.timerId)


 
# Create a render window
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(480,480)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
# Generate an sphere polydata
sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(24)
sphere.SetPhiResolution(24)

sphere.SetStartTheta(0)
epsilon = 1.e-4
sphere.SetEndTheta(360.0-epsilon)

 
# Read the image data from a file
reader = vtk.vtkJPEGReader()
reader.SetFileName(jpegfile)
 
# Create texture object
texture = vtk.vtkTexture()
if vtk.VTK_MAJOR_VERSION <= 5:
    texture.SetInput(reader.GetOutput())
else:
    texture.SetInputConnection(reader.GetOutputPort())

# Map texture coordinates
map_to_sphere = vtk.vtkTextureMapToSphere()

if vtk.VTK_MAJOR_VERSION <= 5:
    map_to_sphere.SetInput(sphere.GetOutput())
else:
    map_to_sphere.SetInputConnection(sphere.GetOutputPort())
map_to_sphere.AutomaticSphereGenerationOn()
#map_to_sphere.PreventSeamOn()
map_to_sphere.PreventSeamOff()

# Create mapper and set the mapped texture as input
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(map_to_sphere.GetOutput())
else:
    mapper.SetInputConnection(map_to_sphere.GetOutputPort())
 
# Create actor and set the mapper and the texture
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)
 
ren.AddActor(actor)
iren.Initialize()
renWin.Render()

cb = vtkTimerCallback(10, actor, iren)
iren.AddObserver('TimerEvent', cb.execute)
timerId = iren.CreateRepeatingTimer(30)
renWin.Render()
iren.Start()

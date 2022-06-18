#Author-
#Description-

from calendar import c
import adsk.core, adsk.fusion, adsk.cam, traceback, math

# radius
r = 0.5
# end angle
theta = 540
# step
n = 180

theta = theta / 180 * math.pi
t = theta / (n * (n - 1) / 2)
px0 = n * r
py0 = 0
cx0 = 0
cy0 = 0
xofs = n * r

app = adsk.core.Application.get()
if app:
    ui = app.userInterface
    product = app.activeProduct
design = adsk.fusion.Design.cast(product)
rootComp = design.rootComponent

def run(context):
    global px0, py0, cx0, cy0
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        pathSketch = sketches.add(xyPlane)
        points = adsk.core.ObjectCollection.create()
        points.add(adsk.core.Point3D.create(px0 - xofs, py0, 0))
        points2 = adsk.core.ObjectCollection.create()
        points2.add(adsk.core.Point3D.create(cx0, cy0, 0))

        for i in range(1, n):
            px = math.cos(i * t) * (px0 - cx0) - math.sin(i * t) * (py0 - cy0) + cx0
            py = math.sin(i * t) * (px0 - cx0) + math.cos(i * t) * (py0 - cy0) + cy0
            cx = (1 - i / (i + 1)) * (px - cx0) + cx0
            cy = (1 - i / (i + 1)) * (py - cy0) + cy0
#            ui.messageBox("px = " + str(px) + ", py = " + str(py))
            points.add(adsk.core.Point3D.create(px - xofs, py, 0))
            points2.add(adsk.core.Point3D.create(cx, cy, 0))
            px0 = px
            py0 = py
            cx0 = cx
            cy0 = cy
        pathSketch.sketchCurves.sketchFittedSplines.add(points)
#        pathSketch.sketchCurves.sketchFittedSplines.add(points2)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

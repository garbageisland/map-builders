import bpy
import random
import math
from time import gmtime, strftime

grid = 8
space = 2.5
seconds = 1
depth = 4
root = '/home/justin/Documents/damp/starmap'
batch = strftime("%y%m%d_%H%M", gmtime())

scene = bpy.context.scene
fps = scene.render.fps
scene.frame_end = fps/scene.frame_step*seconds
loop = scene.frame_end

scene.render.resolution_x = 256
scene.render.resolution_y = 256
scene.render.resolution_percentage = 100
camera_name = 'Camera'

def setupScene():
    bpy.ops.object.select_all(action='DESELECT')
    for item in bpy.data.objects:
        if item.type == 'MESH':
            n = item.name
            bpy.data.objects[n].select = True
            bpy.ops.object.delete()
        elif item.type == 'CAMERA':
            camera_name = item.name

def populateSpace():
    object_primitives = ['cube','torus','uv_sphere','ico_sphere','cylinder','cone']
    last_primitive = len(object_primitives) - 1
    
    for i in range(0,grid):
        for j in range(0,grid):
            
            object = object_primitives[random.randint(0,last_primitive)]
            
            x = i*space
            y = j*space
            z = 0

            eval("bpy.ops.mesh.primitive_%s_add(location=(x,y,z),rotation=(0,0,0))" % object)

            duration = random.randint(fps,loop)
            frame0 = random.randint(0,loop - duration)
            frame1 = frame0 + duration
            
            axis = [random.randint(0,2),0]
            axis[1] = axis[0]
            if axis[0] < 2:
                axis[1] += 1
            else:
                axis[1] -= 1
            
            #it seems animation_data can only support one new action for all data keyframes
            obj = bpy.context.object
            obj.animation_data_create()
            obj.animation_data.action = bpy.data.actions.new(name="rotateAction")

            for k in range(len(axis)):
                euler = ['x','y','z']
                e = eval("bpy.data.objects[obj.name].rotation_euler.%s" % euler[k])
                
                rotate = obj.animation_data.action.fcurves.new(data_path="rotation_euler", index=axis[k])
                rotate.keyframe_points.add(2)
                rotate.keyframe_points[0].co = frame0, e
                rotate.keyframe_points[1].co = frame1, e+(2*math.pi)

def renderScene():
    camera = bpy.data.objects[camera_name]
    offset = space/2
    
    for z in range(depth):
        level = 2**z
        zoom = grid*space/level
        bpy.data.cameras[camera_name].ortho_scale = zoom
        
        for x in range(level):
            increment = zoom/2 - offset
            locx = increment + x*zoom
            camera.location.x = locx

            for y in range(level):
                locy = (grid * space - space) - (increment + y*zoom) #offset spacing is reintorduced somewhere here
                camera.location.y = locy
                
                scene.render.filepath = '%s/render/%s/%s/%s/%s/raw' % (root, batch, z, x, y)
                
                bpy.ops.render.render(animation=True)
                print( "%s(%s),%s(%s),%s(%s), inc=%s" % (zoom,z,locx,x,locy,y,increment))
                
if grid <= 30:
    bpy.ops.text.save()
    setupScene()
    populateSpace()
    bpy.ops.wm.save_mainfile()
    renderScene()
else:
    print("your grid level is set to insane: %s! bump it below 30 or die" % grid)
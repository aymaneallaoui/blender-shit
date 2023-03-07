import bpy
import mathutils
import math

def apollonian_fractal(iterations, a, b, c, d, inside=True):
    
    cube = bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    cube = bpy.context.active_object

   
    sphere1 = bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    sphere1 = bpy.context.active_object
    sphere1.scale = mathutils.Vector((a, a, a))

    sphere2 = bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(b, 0, 0))
    sphere2 = bpy.context.active_object
    sphere2.scale = mathutils.Vector((b, b, b))

    sphere3 = bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(c, d, 0))
    sphere3 = bpy.context.active_object
    sphere3.scale = mathutils.Vector((c, c, c))

    sphere4 = bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(-c, d, 0))
    sphere4 = bpy.context.active_object
    sphere4.scale = mathutils.Vector((d, d, d))

    all_spheres = [sphere1, sphere2, sphere3, sphere4]

    
    for i in range(iterations):
       
        min_radius = min([sphere.scale.x for sphere in all_spheres])

        
        max_indices = []
        for j, sphere in enumerate(all_spheres):
            curvature = 1 / sphere.scale.x
            if abs(curvature - 1 / min_radius) < 0.0001:
                max_indices.append(j)

        
        pos = [0, 0, 0]
        r = 1 / (2 * min_radius - sum([1 / all_spheres[j].scale.x for j in max_indices]))
        for j in max_indices:
            pos[0] += all_spheres[j].location.x * all_spheres[j].scale.x
            pos[1] += all_spheres[j].location.y * all_spheres[j].scale.x
            pos[2] += all_spheres[j].location.z * all_spheres[j].scale.x
        pos = [x / sum([1 / all_spheres[j].scale.x for j in max_indices]) for x in pos]

        new_sphere = bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD')
        new_sphere = bpy.context.active_object
        new_sphere
    new_sphere.location = mathutils.Vector(pos)
    new_sphere.scale = mathutils.Vector((r, r, r))

    
    if inside:
        for sphere in all_spheres:
            dist = (sphere.location - new_sphere.location).length
            if dist < abs(sphere.scale.x - new_sphere.scale.x):
                all_spheres.remove(sphere)
                bpy.data.objects.remove(sphere)

     
    all_spheres.append(new_sphere)

    
    for sphere in all_spheres:
        sphere.select_set(True)
    cube.select_set(True)
    bpy.context.view_layer.objects.active = cube
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
    bpy.context.object.modifiers["Boolean"].object = sphere1
    bpy.ops.object.modifier_apply(modifier="Boolean")

    
    for sphere in all_spheres:
        bpy.data.objects.remove(sphere)

    
    return cube

apollonian_fractal(3, 1, 1, 1, 1)
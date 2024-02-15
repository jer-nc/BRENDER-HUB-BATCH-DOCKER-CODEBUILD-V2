import sys
import os
import bpy

def configure_cycles_denoise(denoise, denoise_algorithm, noise_treshold):
    if denoise:
        bpy.context.scene.cycles.use_denoising = True
        bpy.context.scene.cycles.denoising_radius = noise_treshold

        if denoise_algorithm != "OPENIMAGEDENOISE":
            print("Denoise algorithm not supported, using OPENIMAGEDENOISE instead")
            bpy.context.scene.cycles.denoiser = "OPENIMAGEDENOISE"
        else:
            bpy.context.scene.cycles.denoiser = denoise_algorithm
            print(f"Denoise algorithm set to {bpy.context.scene.cycles.denoiser}")
    else:
        bpy.context.scene.cycles.use_denoising = False
        print("Denoise disabled")

def configure_render_settings(blender_engine, current_frame, resolution_x, resolution_y, color_depth, color_mode, output_format, compression, samples, denoise, denoise_algorithm, noise_treshold, resolution_percentage):
    bpy.context.scene.render.engine = blender_engine
    bpy.context.scene.frame_set(current_frame)
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y
    bpy.context.scene.render.resolution_percentage = resolution_percentage
    bpy.context.scene.render.image_settings.color_depth = color_depth
    bpy.context.scene.render.image_settings.color_mode = color_mode
    bpy.context.scene.render.image_settings.compression = compression
    bpy.context.scene.render.image_settings.file_format = output_format

    if blender_engine == "CYCLES":
        bpy.context.scene.cycles.samples = samples
        bpy.context.scene.cycles.use_denoising = denoise
        bpy.context.scene.cycles.denoising_radius = noise_treshold
        configure_cycles_denoise(denoise, denoise_algorithm, noise_treshold)
    elif blender_engine == "BLENDER_EEVEE":
        bpy.context.scene.eevee.taa_render_samples = samples

def set_scene_objects(scene_name, camera_name, layer_name):
    bpy.context.window.scene = bpy.data.scenes[scene_name]
    bpy.context.scene.camera = bpy.data.objects[camera_name]
    bpy.context.scene.name = scene_name

    if layer_name in bpy.context.scene.view_layers:
        bpy.context.scene.view_layers[layer_name].use = True
    else:
        print(f"Error: View layer '{layer_name}' not found in the scene.")

def configure_compositor(render_output_path):
    compositor_context = bpy.context.scene.node_tree
    if compositor_context:
        file_output_nodes = [node for node in compositor_context.nodes if node.bl_idname == "CompositorNodeOutputFile"]

        for index, file_output_node in enumerate(file_output_nodes):
            file_output_node.base_path = os.path.join(render_output_path, "")
            for slot_index, file_slot in enumerate(file_output_node.file_slots):
                file_slot.path = ""
                prefix = f"compositor/FO_{index}_S_{slot_index}_"
                file_slot.path += f"{prefix}"

def main():
    print("Test from render_animation_dynamic.py")

    # Get command line arguments
    current_frame, blender_engine,blender_file_path,render_output_path,scene_name,layer_name,camera_name, \
    resolution_x,resolution_y,color_depth,color_mode,output_format,compression, \
    samples,denoise,denoise_algorithm,noise_treshold, resolution_percentage = sys.argv[-18:]

    # Cast types from string to their respective types
    current_frame = int(current_frame)
    resolution_x = int(resolution_x)
    resolution_y = int(resolution_y)
    compression = int(compression)
    samples = int(samples)
    denoise = bool(denoise)
    noise_treshold = float(noise_treshold)
    resolution_percentage = int(resolution_percentage)
    current_frame = int(current_frame)

    bpy.ops.wm.open_mainfile(filepath=blender_file_path)
    set_scene_objects(scene_name, camera_name, layer_name)
    configure_compositor(render_output_path)

    bpy.context.scene.cycles.device = "CPU"
    bpy.context.scene.render.filepath = os.path.join(render_output_path, f"{current_frame:05d}")
    bpy.context.scene.render.image_settings.file_format = output_format

    configure_render_settings(blender_engine, current_frame, resolution_x, resolution_y, color_depth, color_mode,
                              output_format, compression, samples, denoise, denoise_algorithm, noise_treshold,
                              resolution_percentage)

    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.quit_blender()

if __name__ == "__main__":
    main()

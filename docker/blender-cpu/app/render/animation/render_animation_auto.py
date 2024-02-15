import bpy
import sys
import os

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

def set_up_render_context(blender_file_path, current_frame):
    bpy.ops.wm.open_mainfile(filepath=blender_file_path)

    bpy.context.scene.frame_set(current_frame)
    current_frame = bpy.context.scene.frame_current
    print(f"Current frame: {current_frame}")
    bpy.context.scene.cycles.device = "CPU"

    # Get denoise settings from scene context
    denoise_enabled = bpy.context.view_layer.cycles.use_denoising
    print(f"Denoise está {'activado' if denoise_enabled else 'desactivado'}")

    # Obtener el tipo de denoise
    denoise_algorithm = bpy.context.scene.cycles.denoiser
    print(f"El tipo de Denoise es {denoise_algorithm}")

    if denoise_enabled and denoise_algorithm != "OPENIMAGEDENOISE":
        print("Denoise está activado pero el tipo de denoise no es OpenImageDenoise. Se establecerá OpenImageDenoise como tipo de denoise.")
        bpy.context.scene.cycles.denoiser = "OPENIMAGEDENOISE"
        denoise_algorithm = bpy.context.scene.cycles.denoiser
        devices = bpy.context.scene.cycles.device
        print(f"Devices: {devices}")
        print(f"El tipo de Denoise es {denoise_algorithm}")
    else:
        print("Denoise: " + denoise_algorithm)
        devices = bpy.context.scene.cycles.device
        print(f"Devices: {devices}")
    
    return current_frame

def set_output_path(output_path, current_frame):
    # Establecer la ruta de salida dinámica
    bpy.context.scene.render.filepath = os.path.join(output_path, f"{current_frame:05d}")

def render_and_save_image():
    # Renderizar la imagen y guardarla en la ruta de salida
    bpy.ops.render.render(write_still=True)

def quit_blender():
    # Salir de Blender después de renderizar
    bpy.ops.wm.quit_blender()

def main():
    print("Test from render_animation_auto.py")
    # Get command line arguments
    current_frame, blender_file_path, output_path = sys.argv[-3:]

    print(blender_file_path)
    print(output_path)
    print(current_frame)

    current_frame = int(current_frame)

    set_up_render_context(blender_file_path, current_frame)

    configure_compositor(output_path)

    set_output_path(output_path, current_frame)

    render_and_save_image()

    quit_blender()
    

if __name__ == "__main__":
    main()
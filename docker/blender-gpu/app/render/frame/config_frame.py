import sys
import json
import os

render_output_path = os.environ['EFS_BLENDER_OUTPUT_FOLDER_PATH']
blender_file_path = os.environ['EFS_BLENDER_FILE_PATH']
blender_executable = os.environ['BLENDER_EXECUTABLE']

def execute_bpy_script(script_args, is_render_auto):
    print("Executing Blender Script")
    print(f"Script Args: {script_args}")

    if is_render_auto:
        render_script = '/app/render/frame/render_frame_auto.py'
        render_command = f'"{blender_executable}" -b -P {render_script} -- {" ".join(script_args)}'
    else:
        render_script = '/app/render/frame/render_frame_dynamic.py'
        render_command = f'"{blender_executable}" -b -P {render_script} -- {" ".join(script_args)}'

    print(f"Render Command: {render_command}")

    os.system(render_command)


def configure_bpy_args(json_data):
    render_config_key = json_data.get('RenderConfig', {})
    print(f"Render Key: {render_config_key}")
    render_frame_key = render_config_key.get("Frame", {})
    print(f"Render Frame Key: {render_frame_key}")

    # Global Render Settings
    is_render_auto = render_config_key.get("isRenderAuto", None)
    blender_engine = render_config_key.get("Engine", None)

    # Frame Specific Settings
    scene_name = render_frame_key.get("SceneName", None)
    layer_name = render_frame_key.get("LayerName", None)
    camera_name = render_frame_key.get("CameraName", None)
    num_frame = render_frame_key.get("NumFrame", None)
    resolution_x = render_frame_key.get("Resolution", {}).get("X", None)
    resolution_y = render_frame_key.get("Resolution", {}).get("Y", None)
    color_depth = render_frame_key.get("ColorDepth", None)
    color_mode = render_frame_key.get("ColorMode", None)
    output_format = render_frame_key.get("OutputFormat", None)
    compression = render_frame_key.get("Compression", None)
    resolution_percentage = render_frame_key.get("ResolutionPercentage", None)
    samples = render_frame_key.get("Samples", None)
    denoise = render_frame_key.get("Denoise", None)
    denoise_algorithm = render_frame_key.get("DenoiseAlgorithm", None)
    noise_treshold = render_frame_key.get("NoiseTreshold", None)

    script_args_auto = [
        blender_file_path,
        render_output_path,
    ]

    script_args_dynamic = [
        blender_engine,
        blender_file_path,
        render_output_path,
        scene_name,
        layer_name,
        camera_name,
        str(num_frame),
        str(resolution_x),
        str(resolution_y),
        str(color_depth),
        color_mode,
        output_format,
        str(compression),
        str(samples),
        str(denoise),
        denoise_algorithm,
        str(noise_treshold),
        str(resolution_percentage),
    ]

    if is_render_auto:
        execute_bpy_script(script_args_auto, is_render_auto)
    else:
        execute_bpy_script(script_args_dynamic, is_render_auto)
    


if __name__ == "__main__":
    print("Test from config_frame.py")
    if len(sys.argv) < 2:
        print("Error: No JSON string provided.")
        sys.exit(1)

    json_str = sys.argv[1]

    json_data = json.loads(json_str)
    print("Parsed JSON in config_frame.py:")
    print(json.dumps(json_data, indent=2))

    configure_bpy_args(json_data)
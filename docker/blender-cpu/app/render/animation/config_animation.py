import sys
import json
import os

render_output_path = os.environ['EFS_BLENDER_OUTPUT_FOLDER_PATH']
blender_file_path = os.environ['EFS_BLENDER_FILE_PATH']
blender_executable = os.environ['BLENDER_EXECUTABLE']

# Get the array index and array size from the environment variables.
int_idx_array = int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])
array_size = int(os.environ['AWS_BATCH_JOB_ARRAY_SIZE'])
job_id = os.environ['AWS_BATCH_JOB_ID'] # Get the job ID to use as a unique identifier ex: 4fce4f74-96e4-4188-a07f-36898cfd75ab:29/
job_id_without_index = job_id.split(':')[0]

print(f"Matrix Index: {int_idx_array}")
print(f"Array Size Job: {array_size}")
print(f"Job ID: {job_id}")
print(f"Job Id Without Index: {job_id_without_index}")

def calculate_current_frame(int_idx_array,start_frame):
        if int_idx_array == 0:
            return start_frame
        else:
            return start_frame + int_idx_array

def execute_bpy_script(script_args, is_render_auto):
    print("Executing Blender Script")
    print(f"Script Args: {script_args}")

    if is_render_auto:
        render_script = '/app/render/animation/render_animation_auto.py'
        render_command = f'"{blender_executable}" -b -P {render_script} -- {" ".join(script_args)}'
    else:
        render_script = '/app/render/animation/render_animation_dynamic.py'
        render_command = f'"{blender_executable}" -b -P {render_script} -- {" ".join(script_args)}'

    print(f"Render Command: {render_command}")

    os.system(render_command)

def configure_bpy_args(json_data):
    render_config_key = json_data.get('RenderConfig', {})
    print(f"Render Key: {render_config_key}")
    render_animation_key = render_config_key.get("Animation", {})
    print(f"Render Frame Key: {render_animation_key}")

    # Global Render Settings
    is_render_auto = render_config_key.get("isRenderAuto", None)
    blender_engine = render_config_key.get("Engine", None)

    # Animation Specific Settings
    scene_name = render_animation_key.get("SceneName", None)
    layer_name = render_animation_key.get("LayerName", None)
    camera_name = render_animation_key.get("CameraName", None)
    start_frame = render_animation_key.get("StartFrame", None)
    end_frame = render_animation_key.get("EndFrame", None)
    fps = render_animation_key.get("FPS", None)
    frame_step = render_animation_key.get("FrameStep", None) # TODO: Implement frame step.
    resolution_x = render_animation_key.get("Resolution", {}).get("X", None)
    resolution_y = render_animation_key.get("Resolution", {}).get("Y", None)
    color_depth = render_animation_key.get("ColorDepth", None)
    color_mode = render_animation_key.get("ColorMode", None)
    output_format = render_animation_key.get("OutputFormat", None)
    compression = render_animation_key.get("Compression", None)
    resolution_percentage = render_animation_key.get("ResolutionPercentage", None)
    samples = render_animation_key.get("Samples", None)
    denoise = render_animation_key.get("Denoise", None)
    denoise_algorithm = render_animation_key.get("DenoiseAlgorithm", None)
    noise_treshold = render_animation_key.get("NoiseTreshold", None)

    script_args_auto = [
        str(current_frame),
        blender_file_path,
        render_output_path,
    ]

    script_args_dynamic = [
        str(current_frame),
        blender_engine,
        blender_file_path,
        render_output_path,
        scene_name,
        layer_name,
        camera_name,
        # str(end_frame),
        # str(fps),
        # str(frame_step),
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
        str(resolution_percentage)
    ]

    if is_render_auto:
        execute_bpy_script(script_args_auto, is_render_auto)
    else:
        execute_bpy_script(script_args_dynamic, is_render_auto)
        

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Error: No JSON string provided.")
        sys.exit(1)

    json_str = sys.argv[1]

    json_data = json.loads(json_str)
    print("Parsed JSON in config_animation.py:")
    print(json.dumps(json_data, indent=2))

    # Calculate the current frame based on the array index.
    start_frame = json_data.get('RenderConfig', {}).get('Animation', {}).get('StartFrame', None)
    print(f"Start Frame: {start_frame}")
    current_frame = calculate_current_frame(int_idx_array,start_frame)
    print(f"Current Frame: {current_frame}")

    configure_bpy_args(json_data)


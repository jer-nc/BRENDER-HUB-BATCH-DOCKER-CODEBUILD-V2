import sys
import json
import os
import subprocess

def configure_virtual_display(json_data):
    if json_data is None:
        return

    engine = json_data.get('RenderConfig', {}).get('Engine', '')

    if engine == "BLENDER_EEVEE":
        os.system('Xvfb :1 -screen 0 1280x720x16 &')
        os.environ['DISPLAY'] = ':1'
        print("Blender EEVEE engine selected")

def get_script_path(render_type):
    script_paths = {
        "Frame": "/app/render/frame/config_frame.py",
        "Animation": "/app/render/animation/config_animation.py",
    }
    return script_paths.get(render_type, None)

def execute_processing(json_data):
    if json_data is None:
        return

    render_type = json_data.get('RenderConfig', {}).get('Type', '')

    print(f"Compute Type: {render_type}")

    script_path = get_script_path(render_type)

    if script_path is None:
        print(f"Unsupported render type: {render_type}")
        return

    subprocess.run(['python3', script_path, json.dumps(json_data)])

if __name__ == "__main__":
    print("Test from render_router.py")

    if len(sys.argv) < 2:
        print("Error: No JSON data provided")
        sys.exit(1)

    json_str = sys.argv[1]

    json_data = json.loads(json_str)
    print("Parsed JSON in render_router.py:")
    print(json.dumps(json_data, indent=2))
    
    configure_virtual_display(json_data)
    execute_processing(json_data)

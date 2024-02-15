import os
import subprocess
import sys
import json

job_action = os.environ['JOB_ACTION_TYPE']

def parse_json(json_str):
    try:
        json_data = json.loads(json_str)
        # print("Parsed JSON:")
        # print(json.dumps(json_data, indent=2)) 
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def get_job_action_path():
    script_paths = {
        "copy_efs": "/app/storage-actions/copy_s3_folder_to_efs.py",
        "clean_efs": "/app/storage-actions/cleanup_efs_and_upload_s3.py",
        "render": "/app/render/render_router.py",
    }
    return script_paths.get(job_action, None)


def execute_processing(json_data):

    script_path = get_job_action_path()

    if script_path is None:
        print(f"Unsupported action: {job_action}")
        return

    if job_action == 'render':
        subprocess.run(['python3', script_path, json.dumps(json_data)])
    else:
        subprocess.run(['python3', script_path])


if __name__ == "__main__":
    # JSON FRAME
    # render_json_str = "{\r\n  \"RenderConfig\": {\r\n    \"Type\": \"Frame\",\r\n    \"isRenderAuto\": false,\r\n    \"Engine\": \"CYCLES\",\r\n    \"Frame\": {\r\n      \"NumFrame\": 1,\r\n      \"SceneName\": \"Scene\",\r\n      \"LayerName\": \"ViewLayer\",\r\n      \"CameraName\": \"Camera\",\r\n      \"AspectRatio\": \"16:9\",\r\n      \"Resolution\": {\r\n        \"X\": 1920,\r\n        \"Y\": 1080\r\n      },\r\n      \"ColorDepth\": \"8\",\r\n      \"ColorMode\": \"RGB\",\r\n      \"OutputFormat\": \"PNG\",\r\n      \"Compression\": 15,\r\n      \"ResolutionPercentage\": 100,\r\n      \"Samples\": 10,\r\n      \"Denoise\": true,\r\n      \"DenoiseAlgorithm\": \"OPENIMAGEDENOISE\",\r\n      \"NoiseTreshold\": 0.01\r\n    }\r\n  }\r\n}"
    
    # JSON ANIMATION
    # render_json_str = "{\r\n  \"RenderConfig\": {\r\n    \"Type\": \"Animation\",\r\n    \"isRenderAuto\": false,\r\n    \"Engine\": \"BLENDER_EEVEE\",\r\n    \"Animation\": {\r\n      \"StartFrame\": 25,\r\n      \"EndFrame\": 250,\r\n      \"FPS\": 25,\r\n      \"SceneName\": \"Scene\",\r\n      \"LayerName\": \"ViewLayer\",\r\n      \"CameraName\": \"Camera\",\r\n      \"AspectRatio\": \"16:9\",\r\n      \"Resolution\": {\r\n        \"X\": 1920,\r\n        \"Y\": 1080\r\n      },\r\n      \"ColorDepth\": \"8\",\r\n      \"ColorMode\": \"RGB\",\r\n      \"OutputFormat\": \"PNG\",\r\n      \"Compression\": 15,\r\n      \"ResolutionPercentage\": 100,\r\n      \"Samples\": 10,\r\n      \"Denoise\": true,\r\n      \"DenoiseAlgorithm\": \"OPENIIMAGEDENOISE\",\r\n      \"NoiseTreshold\": 0.01\r\n    }\r\n  }\r\n}"

    # render_json_str = sys.argv[1]
    render_json_str = sys.argv[1] if len(sys.argv) > 1 else "{}"

    json_data = parse_json(render_json_str)
    execute_processing(json_data)
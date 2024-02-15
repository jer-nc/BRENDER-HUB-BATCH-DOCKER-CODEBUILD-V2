import os
import boto3


bucket_name = os.environ['BUCKET_NAME']
bucket_key = os.environ['BUCKET_KEY']
efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']

print(bucket_name)
print(bucket_key)
print(efs_path)

print(f"Copying project folder from S3: {bucket_name}/{bucket_key}")


s3_client = boto3.client('s3')

try:
    # Listar los objetos en el bucket/key
    response = s3_client.list_objects(Bucket=bucket_name, Prefix=bucket_key)

    # Obtener la lista de objetos
    objects = response.get('Contents', [])

    # Copiar cada objeto a la carpeta de destino de manera recursiva
    for obj in objects:
        obj_key = obj['Key']
        dest_path = os.path.join(efs_path, obj_key)
        
        # Crear la estructura de carpetas si no existe
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Descargar el archivo
        s3_client.download_file(bucket_name, obj_key, dest_path)

    print(f"Project folder copied to {efs_path}")
except Exception as e:
    print(f"Error: {e}")
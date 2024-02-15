#!/bin/bash

REPO_ECR_NAME=$1
BLENDER_VERSIONS=$2
AWS_ACCOUNT_ID=$3
AWS_DEFAULT_REGION=$4

# Function to check if Docker image exists in ECR
image_exists_in_ecr() {
    type=$1
    major_version=$2
    image_exists=$(docker manifest inspect $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$REPO_ECR_NAME:$type-$major_version 2>&1)

    if [[ $image_exists == *"no such manifest"* ]]; then
        echo "false"
    else
        echo "true"
    fi
}

# Function to build and push Docker images
build_and_push_image() {
    type=$1
    version=$2
    major_version=$3
    
    type=$(echo $type | tr '[:upper:]' '[:lower:]')
    echo "Type: $type, Version: $version, Major Version: $major_version"

    # Check if the Docker image already exists in ECR
    exists=$(image_exists_in_ecr $type $major_version)

    if [ "$exists" == "false" ]; then
        echo "Image does not exist in ECR. Building and pushing Docker image."
        
        echo "Building Docker image for $type, version $version, major version $major_version"
        cd docker/blender-$type
        docker build -t $REPO_ECR_NAME:$type-$major_version --build-arg BLENDER_VERSION=$version --build-arg BLENDER_VERSION_MAJOR=$major_version .
        docker tag $REPO_ECR_NAME:$type-$major_version $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$REPO_ECR_NAME:$type-$major_version
        docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$REPO_ECR_NAME:$type-$major_version
        echo "Docker image $type pushed to ECR for version $version"
        cd ../..
    else
        echo "Image already exists in ECR. Skipping build and push for Docker image."
    fi
}

# Loop over Blender versions
IFS=',' read -ra VERSION_ARRAY <<< "$BLENDER_VERSIONS"
echo "Blender versions: $VERSION_ARRAY"
echo "ECR Repo Name: $REPO_ECR_NAME"
echo "AWS Account ID: $AWS_ACCOUNT_ID"
echo "AWS Default Region: $AWS_DEFAULT_REGION"

for version in "${VERSION_ARRAY[@]}"; do
    type=$(echo $version | cut -d'-' -f1)
    major_version=$(echo $version | cut -d'-' -f2)
    version_number="${major_version%.*}"  # Extract the major version
    echo "Type: $type, Version: $version_number, Major Version: $major_version"
    build_and_push_image $type $version_number $major_version
done
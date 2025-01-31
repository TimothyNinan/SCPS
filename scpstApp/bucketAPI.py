from google.cloud import storage

bucket_name = "scpst-images"

# Setup Credentials
credentialsPath = "./keys/smart-camera-parking-system-c2a42430fbfc.json"

# Initialize the client
storage_client = storage.Client.from_service_account_json(credentialsPath)

# Get the bucket
bucket = storage_client.bucket(bucket_name)

def upload_to_bucket(image_path, destination_blob_name):
    # Create a new blob and upload the file's content
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(image_path)

    print(f"File {image_path} uploaded to {destination_blob_name}.")

def download_from_bucket(destination_blob_name, local_file_path):
    # Create a new blob and download the file's content to a local file
    blob = bucket.blob(destination_blob_name)
    blob.download_to_filename(local_file_path)

    print(f"File {destination_blob_name} downloaded to {local_file_path}.")

    #return the time the file was uploaded
    return blob.time_created

def get_blob_url(destination_blob_name):
    blob = bucket.blob(destination_blob_name)
    return blob.public_url

def delete_from_bucket(destination_blob_name):
    # Create a new blob and upload the file's content
    blob = bucket.blob(destination_blob_name)
    blob.delete()

    print(f"File {destination_blob_name} deleted.")

def list_bucket():
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        print(blob.name)

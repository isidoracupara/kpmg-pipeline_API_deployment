from io import BytesIO
import os
from azure.storage.blob import BlobServiceClient, ContainerClient
import pandas as pd

CONTAINER_NAME = "CONTAINER NAME"
# LOCAL_PATH = "./data"

def download_csv_files_to_dataframe():
    try:    
        # get connection string
        connect_str = os.getenv('AZURE_CONNECTION_STRING')

        # Create the BlobServiceClient object
        blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(connect_str)

        # Create the BlobClient object
        container_client: ContainerClient = blob_service_client.get_container_client(CONTAINER_NAME)

        # Create a local directory to hold blob data (csv's)
        # if os.path.exists(LOCAL_PATH) == False:
        #     os.mkdir(LOCAL_PATH)
        
        container_client = blob_service_client.get_container_client(container=CONTAINER_NAME) 
        
        df = pd.DataFrame()

        for blob in container_client.list_blobs():
            # download_file_path = os.path.join(LOCAL_PATH, blob.name)
            # print("Downloading blob to: \t" + download_file_path + "\n")
 
            # with open(download_file_path, "wb") as file:
            #     file.write(container_client.download_blob(blob.name).readall())

            with BytesIO() as blob_data:
                container_client.download_blob(blob.name).download_to_stream(blob_data)
                blob_data.seek(0)
                downloaded_df = pd.read_csv(blob_data)
                pd.concat([df,downloaded_df])
                
        return df

    except Exception as ex:
        print('Exception:')
        print(ex)

   
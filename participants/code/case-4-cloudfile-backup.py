from config import get_config
import subprocess
from datetime import datetime
from io import BytesIO

from libcloud.storage.types import Provider, ContainerDoesNotExistError
from libcloud.storage.providers import get_driver

config = get_config()
identity = config["identity"]
credential = config["credential"]
rgn = config["region"]

# Connect to Rackspace Cloud Files in the IAD datacenter.
Driver = get_driver(Provider.CLOUDFILES)
storage = Driver(identity, credential, region=rgn)

# Create a new container within Rackspace Cloud Files.
container = storage.create_container("riddhi_container")

# Upload some data to our new container.
# If you're uploading files that are represented on disk, 
# you can use storage.upload_object which takes a file name.
obj = container.upload_object_via_stream(BytesIO("riddhi_sample_data"),
                                         object_name="riddhi_uploaded_data")
print("Data successfully uploaded to the container")
# Return our specific container.
# If we didn't already know the name, we could `list_containers()`.
container = storage.get_container("riddhi_container")
obj = container.get_object("riddhi_uploaded_data")

# as_stream returns a generator of our data.
stream = obj.as_stream()
data = next(stream) # `data` is now "some_data", as we uploaded.
print('The data that I had backed up in Cloud Files is',str(data))
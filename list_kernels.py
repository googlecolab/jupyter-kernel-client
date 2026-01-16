import os
from jupyter_kernel_client import KernelClient

# Replace with your Jupyter Server URL and token
SERVER_URL = "http://localhost:8888"
TOKEN = "1cd66f8f48ffaf1efca5bd76bc1509c56195bb931ac0ceeb"

# You don't need to specify a kernel_id if you just want to list kernels.
# The client will use the server_url and token to connect to the Jupyter Server API.
client = KernelClient(server_url=SERVER_URL, token=TOKEN)

try:
    print(f"Attempting to list kernels from {SERVER_URL}...")
    running_kernels = client.list_kernels()

    if running_kernels:
        print("\nFound the following running Jupyter Kernels:")
        for i, kernel in enumerate(running_kernels):
            print(f"{i+1}. ID: {kernel.get('id')}, Name: {kernel.get('name')}, Last Activity: {kernel.get('last_activity')}")
    else:
        print("\nNo running Jupyter Kernels found.")

except Exception as e:
    print(f"\nAn error occurred while trying to list kernels: {e}")

# The client instance doesn't manage a specific kernel for listing,
# so there's no need to call client.stop() unless you had also started a kernel.

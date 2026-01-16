
import os
from datetime import datetime, timezone
from jupyter_kernel_client import KernelClient

# Replace with your Jupyter Server URL and token
SERVER_URL = os.environ.get("JUPYTER_SERVER_URL", "http://localhost:8888")
TOKEN = os.environ.get("JUPYTER_TOKEN", "MY_TOKEN")

def parse_activity_time(timestamp_str):
    """Parses the ISO 8601 timestamp string from the kernel manager."""
    # The timestamp format is like '2024-03-20T19:39:13.123456Z'
    return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

def main():
    """Finds and executes code on the most recently active Jupyter kernel."""
    # 1. Use a client to discover available kernels
    # No kernel_id is provided, so this client only queries the server API.
    listing_client = KernelClient(server_url=SERVER_URL, token=TOKEN)

    most_recent_kernel = None
    latest_activity = datetime.min.replace(tzinfo=timezone.utc)

    try:
        print("Discovering running kernels...")
        running_kernels = listing_client.list_kernels()

        if not running_kernels:
            print("No running kernels found.")
            return

        # 2. Find the kernel with the most recent activity
        for kernel in running_kernels:
            last_activity_time = parse_activity_time(kernel.get("last_activity", ""))
            if last_activity_time > latest_activity:
                latest_activity = last_activity_time
                most_recent_kernel = kernel

        if most_recent_kernel:
            kernel_id = most_recent_kernel.get("id")
            kernel_name = most_recent_kernel.get("name")
            print(f"\nFound most recently active kernel:")
            print(f"  ID: {kernel_id}")
            print(f"  Name (Type): {kernel_name}")
            print(f"  Last activity: {latest_activity.isoformat()}")

            # Verify it's a Python kernel
            if not kernel_name.lower().startswith("python"):
                print(f"\nSelected kernel '{kernel_name}' is not a Python kernel. Exiting.")
                return

            # 3. Connect to the specific kernel using a context manager
            print("\nConnecting to this kernel...")

            # The 'with' statement automatically handles calling start() and stop().
            # Because we provide a 'kernel_id', the client knows it doesn't "own"
            # the kernel, so stop() will not shut it down by default.
            with KernelClient(server_url=SERVER_URL, token=TOKEN, kernel_id=kernel_id) as execution_client:

                code_to_run = "import platform; print(f'Hello from an existing kernel running on {platform.node()}!')"
                print(f"Executing code:\n---\n{code_to_run}\n---")

                # 4. Execute code
                reply = execution_client.execute(code_to_run)

                # 5. Print the output from the kernel
                print("\nExecution reply from kernel:")
                if reply and reply.get('outputs'):
                    for output in reply['outputs']:
                        if output['output_type'] == 'stream':
                            print(output['text'].strip())
                else:
                    print("Received no output, but execution status was:", reply.get('status'))

            print("\nClient connection closed.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

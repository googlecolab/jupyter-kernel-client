import logging
import time

from jupyter_kernel_client import KernelClient
from jupyter_kernel_client import JupyterSubprotocol

#logging.basicConfig(level=logging.DEBUG)

SERVER = "https://8080-m-s-kkb-use1d2-1httwdf8jex0i-d.us-east1-2.sandbox.colab.dev"
KERNEL = "da2c6380-6867-4a62-843f-8b3204883566"
TOKEN  = "eyJhbGciOiJFUzI1NiIsImtpZCI6Im9xcTRPdyJ9.eyJhdWQiOiJtLXMta2tiLXVzZTFkMi0xaHR0d2RmOGpleDBpIiwiZXhwIjoxNzY3ODE5OTc3LCJwb3J0Ijo4MDgwfQ.leSLCNeiFY9-GXMHYdYOy0erwbinpCXDBViz7dZ82kSfTCmXYzJVJ7SpDPDuRmm9kAFtAAERjm4mymryuyT5Kw"

with KernelClient(
        server_url=SERVER,
        kernel_id=KERNEL,
        token='unused',
        client_kwargs = {
            'subprotocol': JupyterSubprotocol.JSON,
        },
        headers = {
            'X-Colab-Client-Agent': 'colab-mcp',
            'X-Colab-Runtime-Proxy-Token': TOKEN,
        }
        ) as kc:
    reply = kc.execute("print('hey')")
    print(reply)

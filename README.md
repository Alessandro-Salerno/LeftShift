# LeftShift
LeftShift is a simple work-in-progress protocol used to send and receive JSON-like data using HTTP POST Requests and responses.
It is designed to be easy and quick to set up and currently offers very little.
The protocol is designed to work across any language and platform, as such, it only transfers text and Request Headers, but no python-specific binary data.

## Project Structure
LeftShift is structured as a Python Package, as such, it has to be installed via the pip package manager.

## Building LeftShift
### Requirements
* Python 3.7 or newer
* The Python `build` module
* The `hatchling` backend
### Procedure
* Clone this repository
* Run the `build` module via Python (`python3 -m build` on macOS/Linux, `py -m build`  on Windows)
* Install LeftShift using `pip` and the `.whl` in the `dist` directory

## The LeftShift Protocol
Currently, the LeftShift Protocol is very simple and basic: it uses the JSON format to send and receive information and provides two identical (For now) types: `LeftShiftRequest` and `LeftShiftResponse`. A LeftShift Request/Response only contains the content and its type.

## Using LeftShift in a Python Project
### Writing a makeshift server
```py
# Import the LeftShift package
import leftshift


# Create a LeftShift Server instance on localhost:8000
leftshift_server = leftshift.LeftShiftServer('', 8000)

# Start the server (The library will automatically spawn a new thread)
leftshift_server.run()

# Create a handler for a 'ping-pong-request'
# This handler will send back the client's message (content)
@leftshift_server.handler('ping-pong-request')
def ping_pong_handler(content):
    return leftshift.LeftShiftResponse(
        content_type='ping-pong-response',
        content=f'ping-pong {content}'
    )

```

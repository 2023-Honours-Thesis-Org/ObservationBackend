# Credits
I'd like to acknowlegde the increadible work done by developers of [firendlyVRI](https://github.com/crpurcell/friendlyVRI),
Cormac R. Prucell ([@crpurcell](https://github.com/crpurcell)) & Roy Truelove, backend logic and functions used to generate
simulation images are from their project an was wrapped around in python to work as a REST API that can interface

**Harikesha Suresh**

**`h.suresh@uqconnect.edu.au`**

# Observation Backend
The backend service for processing telescope images as a radio telescope would.

# To Demo

The API is dockerised and works best in that environment so the only dependency would be 
Docker itself, run the following command under projects root directory.

```bash
$ docker-compose up --build
```

To demo the API functionality, I've provided an instance of Jupyter Lab with the 
`API_Testing_Docker.ipynb` notebook that call's all the APIs functions and displays results, 
to access it, navigate to `http://localhost:4841/` in your browser after running the command 
above, it should be the only file in the directory tree.

Alternatively, you can just use the `JupyterTesting/API_Test.ipynb` notebook if you have a 
local instance of JupyterLab running.

The demo uses two array configurations from the Very Large Array (VLA), there are configuration
options for ATCA and ASKAP.

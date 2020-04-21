# Fantraxpy API Client (Unofficial)
An API client for Fantrax.com fantasy sports website.

Unfortunately, Fantrax has updated their website and use reCAPTCHA so webscrapping isn't possible without way more work then I'm willing to put in. 
*THIS WILL NOT BE ABLE TO LOG IN AND THEREFORE IT DOES NOT WORK.*

## Setup
First: create a conda environment with from the environment yaml.

Second: Activate the environment and set your fantrax API token. You can find this by going to developer tools in your browser and settings and then click on the network tab. Your token will be in one of the request headers.
```bash
conda activate fantrax-env
export FANTAX_TOKEN="put-your-fantrax-token-here"
```

## Usage:
```python
import fantraxpy as ftx

fantrax = Fantrax(username='fantrax_username',
                  password='fantrax_password')
```

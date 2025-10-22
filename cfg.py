import yaml
import os

config_dir = os.path.join(os.path.dirname(__file__))
config_file = os.path.join(config_dir, 'config.yaml')

def read_config(config_file):
    with open(config_file, 'r') as f: config = yaml.load(f, Loader=yaml.FullLoader)
    return config

config = read_config(config_file)

REPLICATE_key = config["replicate"]["api_key"]
NO_PICS = 1

DEFAULT_MODEL = "schnell"
URL = "https://api.replicate.com/v1/models/"
rep_models = {
        "schnell":"black-forest-labs/flux-schnell", 
        "flux":"black-forest-labs/flux-pro",
        "kontext-pro":"black-forest-labs/flux-kontext-pro", 
        "schnell-lora":"black-forest-labs/flux-schnell-lora",
        "flux-pro":"black-forest-labs/flux-1.1-pro",
        "flux-pro-ultra":"black-forest-labs/flux-1.1-pro-ultra",
        "flux-dev":"black-forest-labs/flux-dev",
        "sd3":"stability-ai/stable-diffusion-3",
        "seedream":"bytedance/seedream-4",
        "imagen":"google/imagen-4-ultra/",
        "banana":"google/nano-banana",
        "kontext-max":"black-forest-labs/flux-kontext-max",
        }

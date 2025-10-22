import asyncio
import argparse
import datetime
import io, os
from PIL import Image
import requests
from cfg import *

async def imagine(title, prompt, model, n):
    dir_path = f'./output/'
    if not os.path.exists(dir_path): os.makedirs(dir_path)
    if n < 1: n = NO_PICS
    for i in range(n):
            try: binary = await generate_image(prompt, model)
            except Exception as e:
                print(e)
                continue
            try: img = Image.open(io.BytesIO(binary))
            except: img = Image.open(binary)
            img.save(f'{dir_path}{title}_{model}_{i}.png')
            print("Prediction succeeded, Image saved.")
    return True


async def generate_image(prompt, model):
    #print("polling",URL,model,"with Prompt:",prompt)
    binary = await replicate_poll(prompt, model)
    return binary


async def replicate_poll(prompt, model=DEFAULT_MODEL):
    if model not in rep_models: model = DEFAULT_MODEL
    m = rep_models[model]
    if "imagen" in model: aspect_ratio = "3:4"
    else: aspect_ratio = "2:3"
    cargo = {
                "prompt": prompt,
                "output_format": "png",
                "aspect_ratio" : aspect_ratio,
    }
    if "schnell" in model: 
        cargo.update({
                "disable_safety_checker": True
            }
        )
    else:
        cargo.update({
                "safety_tolerance":6
            }
        )
    payload = {"input": cargo}
    url = f"{URL}{m}/predictions"
    print("polling replicate at", url)
    response = await asyncio.to_thread(requests.post,
        url,
        headers={
            "Authorization": f"Bearer {REPLICATE_key}",
            "Content-Type": "application/json"
        },
        json=payload  # Use json= instead of data=
    )

    if response.status_code != 201:  # 201 is the status code for a created resource
        raise Exception(str(response.json()))

    get_url = response.json()["urls"]["get"]
    
# Polling for the prediction result
    while True:
        poll_response = await asyncio.to_thread(requests.get, get_url, headers={
            "Authorization": f"Bearer {REPLICATE_key}"
        })
        
        if poll_response.status_code != 200:
            raise Exception(str(poll_response.json()))
        
        poll_data = poll_response.json()
        if poll_data["status"] == "succeeded":
            # The output is typically a list of URLs to the generated images
            output = poll_data["output"]
            if isinstance(output, str): image_url = output
            else: image_url = output[0]
                # Fetch the first image content from the list of output URLs
            image_response = await asyncio.to_thread(requests.get, image_url)
            return image_response.content

        elif poll_data["status"] == "failed":
            raise Exception(f"Prediction failed: {poll_data['error']}") #)
        
        # Wait for a short period before polling again
        await asyncio.sleep(2)


def main(prompt, title, model, n):
    asyncio.run(imagine(prompt, title, model, n))


if __name__ == "__main__":
    current_date = datetime.date.today()
    date_string = current_date.strftime("%Y-%m-%d-%H-%M")
    parser = argparse.ArgumentParser(description='App to generate smut in docx with covers in png.')
    parser.add_argument('--prompt', required=True, help='Submit image prompt.')
    parser.add_argument('--n', required=False, help='Number of images to generate.', default=NO_PICS)
    parser.add_argument('--title', required=False, help='Image title.', default=date_string)
    parser.add_argument('--model', required=False, help='Name of image model.', default=DEFAULT_MODEL)

    args = parser.parse_args()
    prompt = args.prompt
    title = args.title
    model = args.model
    n = int(args.n)

    main(title, prompt, model, n)


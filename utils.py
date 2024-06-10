import base64


def encoding_img(path):
    with open(path, 'rb') as image_file:
        image_data =  base64.b64encode(image_file.read()).decode('utf-8')

    return image_data

def retrieve_current_image():
    output =  [{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{encoding_img('current_log.jpg')}"}}]
    return output

def retrieve_sequence_past_images():
    images = ['current_log.jpg','historical_log_1.jpg','historical_log_2.jpg','historical_log_3.jpg']
    output = [{"type":"text","text":"Make your analysis based on this sequence of images."}]

    for image in images:
        output.append({"type": "image_url", "image_url":{"url":f"data:image/jpg;base64,{encoding_img(image)}"}})

    return output
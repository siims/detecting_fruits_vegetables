import base64
import os
from io import BytesIO

import requests
from typing import List

from models import Label
from models import Result
from models import Source

GOOGLE_VISION_API_URL = 'https://cxl-services.appspot.com/proxy?url=https://vision.googleapis.com/v1/images:annotate'


def google_vision_api_request(image):
    """
    Example return object: 
    {
      'responses': [
        {
          'labelAnnotations': [
            {
              'topicality': 0.9552298,
              'description': 'natural foods',
              'mid': '/m/08tlbj',
              'score': 0.9552298
            },
            {
              'topicality': 0.9251235,
              'description': 'fruit',
              'mid': '/m/02xwb',
              'score': 0.9251235
            }
          ]
        }
      ]
    }
    """
    payload = {'requests': [{'image': {'content': to_base64(image)}, 'features': [{'type': 'LABEL_DETECTION'}]}]}
    request = requests.post(GOOGLE_VISION_API_URL, json=payload)
    if request.status_code is not 200:
        print('Request failed to', Source.google_vision_api, request.status_code, request.reason)
        return None

    return request.json()


def parse_response(results) -> List[Label]:
    result_list = []
    for element in results['responses'][0]['labelAnnotations']:
        result_list.append(Label(element['description'], element['score']))
    return result_list


def get_results_for_images(images) -> List[Result]:
    results = []
    for image in images:
        json_response = google_vision_api_request(image)
        labels = parse_response(json_response)
        results.append(Result(os.path.split(image.filename)[1], labels))
    return results


def to_base64(image) -> str:
    buffered = BytesIO()
    image.save(buffered, format='JPEG')
    return base64.b64encode(buffered.getvalue()).decode()

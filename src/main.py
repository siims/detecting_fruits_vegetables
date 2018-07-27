import json
import os
from datetime import datetime

from PIL import Image
from typing import List

import google_vision
from models import Source


def collect_images() -> List[Image.Image]:
    images = []
    for filename in os.listdir('images'):
        images.append(Image.open(os.path.join('images', filename)))

    return images


def results_to_json(results):
    return json.dumps(results, default=lambda o: o.__dict__)


def save_results(results, source) -> None:
    date = datetime.now().date()
    json_data = results_to_json(results)
    with open(os.path.join('results', '%s__%s.json' % (date, source.name)), 'w') as save_file:
        save_file.write(json_data)


if __name__ == '__main__':
    images = collect_images()
    results = google_vision.get_results_for_images(images)
    print('\n'.join(map(str, results)))
    save_results(results, Source.google_vision_api)

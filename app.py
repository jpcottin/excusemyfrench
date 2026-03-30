import base64
import json
import mimetypes
import os
import random
from functools import lru_cache

from flask import (Flask, abort, jsonify, render_template,
                   send_from_directory)

app = Flask(__name__)

# Load insults from JSON file
INSULTS_PATH = os.path.join(app.root_path, 'data', 'insults.json')
with open(INSULTS_PATH, 'r', encoding='utf-8') as f:
    insultes = json.load(f)

IMAGE_FOLDER = 'image/'
STATIC_IMAGE_PATH = os.path.join(app.root_path, 'static', IMAGE_FOLDER)

@lru_cache(maxsize=1)
def get_all_images():
    """List all images in the static image folder. Cached for performance."""
    if not os.path.exists(STATIC_IMAGE_PATH):
        return []
    return sorted([f for f in os.listdir(STATIC_IMAGE_PATH)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])

@app.route("/")
def index():
    insulte = random.choice(insultes)
    return render_template('simple.html', quote=insulte)

@app.route("/api")
def api():
    insulte = random.choice(insultes)
    return jsonify({"result": insulte})

@app.route("/api/v1")
def apiv1():
    random_index = random.randrange(len(insultes))
    return jsonify({
        "insult": {
            "text": insultes[random_index],
            "index": random_index
        }
    })

@app.route("/api/v1/img")
def apiv1img():
    try:
        all_images = get_all_images()
        if not all_images:
            return "No images found", 404

        random_index = random.randrange(len(insultes))
        random_img_index = random.randrange(len(all_images))

        image_name = all_images[random_img_index]
        image_path = os.path.join(STATIC_IMAGE_PATH, image_name)

        with open(image_path, 'rb') as image_file:
            image_64_encode = base64.b64encode(image_file.read()).decode('utf-8')

        mimetype, _ = mimetypes.guess_type(image_path)

        return jsonify({
            "insult": {
                "text": insultes[random_index],
                "index": random_index
            },
            "image": {
                "data": image_64_encode,
                "mimetype": mimetype or "image/jpeg",
                "indexImg": random_img_index
            }
        })

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return "Internal Server Error", 500

@app.route("/img")
def img():
    all_images = get_all_images()
    if not all_images:
        return "No images found", 404

    random_index = random.randrange(len(insultes))
    random_img_index = random.randrange(len(all_images))

    return render_template(
        'img.html',
        quote=insultes[random_index],
        image=IMAGE_FOLDER + all_images[random_img_index],
        ins=random_index,
        imgNumber=random_img_index
    )

@app.route("/series")
def series():
    all_images = get_all_images()
    insulte = random.choice(insultes)
    image_name = random.choice(all_images) if all_images else ""
    return render_template('series.html', quote=insulte, image=IMAGE_FOLDER + image_name)

@app.route("/img/<int:quo>/<int:img>/")
def ins(quo, img):
    all_images = get_all_images()
    try:
        insulte = insultes[quo]
        image_name = all_images[img]
        return render_template('img_noencore.html', quote=insulte, image=IMAGE_FOLDER + image_name)
    except IndexError:
        abort(404)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.errorhandler(500)
def internal_error(error):
    return "500 error", 500

@app.errorhandler(404)
def not_found(error):
    return "404 error", 404

@app.errorhandler(401)
def not_authorized(error):
    return "401 error", 401

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

import base64
import json
import logging
import mimetypes
import os
import random
from functools import lru_cache
from typing import Any, Dict, List, Tuple, Union

from flask import (Flask, Response, abort, jsonify, render_template,
                   request, send_from_directory)

from config import Config

# Configure logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

DEFAULT_LEVEL = 3

def load_insults() -> List[Dict[str, Any]]:
    """Load the insults dataset from JSON.

    Each entry is {"text": str, "level": int} where level 1 is family-friendly,
    2 is vulgar and 3 is offensive.
    """
    try:
        with open(app.config['INSULTS_PATH'], 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load insults: {e}")
        return []

insultes: List[Dict[str, Any]] = load_insults()

def get_max_level() -> int:
    """Read the optional ?level= query parameter.

    Levels are cumulative: level=1 serves only level 1, level=2 serves
    levels 1 and 2, level=3 (the default) serves everything.
    """
    raw = request.args.get('level')
    if raw is None:
        return DEFAULT_LEVEL
    if raw not in ('1', '2', '3'):
        abort(400, description="level must be 1, 2 or 3")
    return int(raw)

def pick_random_insult(max_level: int) -> Tuple[int, Dict[str, Any]]:
    """Pick a random insult of at most max_level.

    Returns (index, insult) where index is the position in the full list,
    so indices stay stable regardless of the level filter.
    """
    eligible = [i for i, ins in enumerate(insultes) if ins['level'] <= max_level]
    index = random.choice(eligible)
    return index, insultes[index]

@lru_cache(maxsize=1)
def get_all_images() -> List[str]:
    """List all images in the static image folder. Cached for performance."""
    static_img_path = app.config['STATIC_IMAGE_PATH']
    if not os.path.exists(static_img_path):
        logger.warning(f"Image directory not found: {static_img_path}")
        return []
    return sorted([f for f in os.listdir(static_img_path)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])

@app.route("/")
def index() -> str:
    if not insultes:
        return render_template('simple.html', quote="No insults available")
    _, insulte = pick_random_insult(get_max_level())
    return render_template('simple.html', quote=insulte['text'])

@app.route("/api")
def api() -> Response:
    if not insultes:
        return jsonify({"result": ""})
    _, insulte = pick_random_insult(get_max_level())
    return jsonify({"result": insulte['text']})

@app.route("/api/v1")
def apiv1() -> Union[Response, Tuple[Response, int]]:
    if not insultes:
        return jsonify({"error": "No insults available"}), 500
    random_index, insulte = pick_random_insult(get_max_level())
    return jsonify({
        "insult": {
            "text": insulte['text'],
            "index": random_index,
            "level": insulte['level']
        }
    })

@app.route("/api/v1/img")
def apiv1img() -> Union[Response, Tuple[str, int]]:
    # Parse the level outside the try block so an invalid value
    # returns 400 instead of being swallowed as a 500.
    max_level = get_max_level()
    try:
        all_images = get_all_images()
        if not all_images:
            return "No images found", 404

        if not insultes:
            return "No insults available", 500

        random_index, insulte = pick_random_insult(max_level)
        random_img_index = random.randrange(len(all_images))

        image_name = all_images[random_img_index]
        image_path = os.path.join(app.config['STATIC_IMAGE_PATH'], image_name)

        with open(image_path, 'rb') as image_file:
            image_64_encode = base64.b64encode(image_file.read()).decode('utf-8')

        mimetype, _ = mimetypes.guess_type(image_path)

        return jsonify({
            "insult": {
                "text": insulte['text'],
                "index": random_index,
                "level": insulte['level']
            },
            "image": {
                "data": image_64_encode,
                "mimetype": mimetype or "image/jpeg",
                "indexImg": random_img_index
            }
        })

    except Exception as e:
        logger.error(f"An error occurred in apiv1img: {str(e)}", exc_info=True)
        return "Internal Server Error", 500

@app.route("/img")
def img() -> Union[str, Tuple[str, int]]:
    all_images = get_all_images()
    if not all_images:
        return "No images found", 404

    if not insultes:
        return "No insults available", 500

    random_index, insulte = pick_random_insult(get_max_level())
    random_img_index = random.randrange(len(all_images))

    return render_template(
        'img.html',
        quote=insulte['text'],
        image=app.config['IMAGE_FOLDER'] + all_images[random_img_index],
        ins=random_index,
        imgNumber=random_img_index
    )

@app.route("/series")
def series() -> str:
    all_images = get_all_images()
    if not insultes:
        return render_template('series.html', quote="", image="")
    _, insulte = pick_random_insult(get_max_level())
    image_name = random.choice(all_images) if all_images else ""
    return render_template('series.html', quote=insulte['text'], image=app.config['IMAGE_FOLDER'] + image_name)

@app.route("/img/<int:quo>/<int:img>/")
def ins(quo: int, img: int) -> Union[str, Tuple[str, int]]:
    all_images = get_all_images()
    try:
        insulte = insultes[quo]
        image_name = all_images[img]
        return render_template('img_noencore.html', quote=insulte['text'], image=app.config['IMAGE_FOLDER'] + image_name)
    except IndexError:
        abort(404)
        return "Not found", 404

@app.route('/favicon.ico')
def favicon() -> Response:
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.errorhandler(400)
def bad_request(error: Any) -> Tuple[Response, int]:
    return jsonify({"error": error.description}), 400

@app.errorhandler(500)
def internal_error(error: Any) -> Tuple[str, int]:
    return "500 error", 500

@app.errorhandler(404)
def not_found(error: Any) -> Tuple[str, int]:
    return "404 error", 404

@app.errorhandler(401)
def not_authorized(error: Any) -> Tuple[str, int]:
    return "401 error", 401

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port)

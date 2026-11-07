import json
import os

import redis
import requests
import yaml
from flask import Flask, jsonify, request


config_path = os.getenv("CONFIG_PATH", "/etc/cache-api/config.yaml")

with open(config_path, "r") as file:
    config = yaml.safe_load(file)

app = Flask(__name__)

cache = redis.Redis(
    host=config["redis"]["host"],
    port=int(config["redis"]["port"]),
    password=config["redis"]["password"],
    decode_responses=True,
)

backend_host = config["backend"]["host"]
backend_port = int(config["backend"]["port"])


@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    cached = cache.get(user_id)

    if cached:
        return jsonify({
            "cached": True,
            "user": json.loads(cached),
        })

    response = requests.get(
        f"http://{backend_host}:{backend_port}/user",
        params={"id": user_id},
        timeout=5,
    )

    if response.status_code == 200:
        cache.set(user_id, response.text, ex=60)

        return jsonify({
            "cached": False,
            "user": response.json(),
        })

    return response.text, response.status_code


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(config["app"]["port"]),
    )

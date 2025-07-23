from flask import Flask, request, redirect, url_for, render_template_string, jsonify
import uuid
import os
import redis
import json
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route("/submit", methods=["POST"])
def submit():
    job_id = str(uuid.uuid4())
    input_data = request.form["input"]
    time_submitted = datetime.now(ZoneInfo("America/Chicago")).isoformat()
    job_type = "reverse"

    job = {
    "job_id": job_id,
    "job_type": job_type,
    "input": input_data,
    "status": "queued",
    "submitted_at": time_submitted
    }

    r.rpush("jobs", json.dumps(job))

    return jsonify(job)


@app.route("/status/<job_id>")
def status(job_id):
    jobs = r.lrange("jobs", 0, -1)
    for job_json in jobs:
        job = json.loads(job_json)
        if job.get("job_id") == job_id:
            return jsonify(job)
        
    return jsonify({
    "job_id": job_id,
    "status": "unknown",
    "info": "Not found in queue — may be processing or completed"
})

app.run(host="0.0.0.0", port=5000)
print("running")
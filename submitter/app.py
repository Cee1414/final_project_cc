from flask import Flask, request, redirect, url_for, render_template_string, jsonify
from controllers import submit_controller
from shared_services.redis import queue
import json
import boto3
import os


dynamodb = boto3.client("dynamodb")

app = Flask(__name__)

TABLE_NAME = os.getenv("TABLE_NAME", "jobs")

print("waiting for table coannection")
dynamodb.get_waiter('table_exists').wait(TableName=TABLE_NAME)
print(f"connected to '{TABLE_NAME}' table successfully.")

@app.route("/submit", methods=["POST"])
def submit():
    input_data = request.form.get("input")
    if not input_data:
        return jsonify({"error": "Missing input"}), 400

    job = submit_controller.handle_submit(input_data)

    return jsonify(job), 202


# @app.route("/redis_status/<job_id>")
# def status(job_id):
#     jobs = r.lrange("jobs", 0, -1)
#     for job_json in jobs:
#         job = json.loads(job_json)
#         if job.get("job_id") == job_id:
#             return jsonify(job)
        
#     return jsonify({
#     "job_id": job_id,
#     "status": "unknown",
#     "info": "Not found in queue, may be processing or completed"
# })

@app.route("/redis_status")
def status():
    try:
        raw_jobs = queue.get_all_jobs()
        jobs = [json.loads(job_str) for job_str in raw_jobs]
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
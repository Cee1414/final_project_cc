from flask import Flask, request, redirect, url_for, render_template_string, jsonify, render_template
from controllers import submit_controller
import os
from shared_services.dynamodb.client import dynamodb_client
from controllers.status_controller import get_redis_status, get_dynamodb_status
from flask_cors import CORS
from shared_services.dynamodb import job_io

app = Flask(__name__)

TABLE_NAME = os.getenv("TABLE_NAME", "jobs")

print("waiting for table coannection")
dynamodb_client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
print(f"connected to '{TABLE_NAME}' table successfully.")

#@app.route("/submit", methods=["POST"])
#def submit():
#    data = request.get_json(silent=True) or {}
#    input_data = data.get("input") or request.form.get("input")
#    if not input_data and request.data:
#        input_data = request.data.decode("utf-8").strip()
#    if not input_data:
#        return jsonify({"error": "Missing input"}), 400
#    job = submit_controller.handle_submit(input_data)
#    return jsonify(job), 202

@app.route("/submit", methods=["POST"])
def submit():
    # 1) Try JSON with {"input": ...}
    data = request.get_json(silent=True) or {}
    input_data = data.get("input")

    # 2) If not JSON, build input from form fields (your current frontend)
    if input_data is None:
        form_dict = request.form.to_dict()  # e.g., task, created_by, iterations
        file_info = None
        if "file" in request.files:
            f = request.files["file"]
            # Don't read/keep the whole file now—just record basic info
            file_info = {
                "file_name": f.filename,
                "content_type": f.mimetype,
                "binary_data": f.read().decode(errors='ignore')
                # optional: uncomment to get size (rewind if you read)
                # "size": len(f.read()); f.stream.seek(0)
            }
        input_data = {**form_dict}
        
        if file_info:
            input_data["file"] = file_info

    if not input_data:
        return jsonify({"error": "Missing input"}), 400

    # Your existing submit logic
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
def redis_status():
    try:
        jobs = get_redis_status()
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/dynamodb_status")
def dyamodb_status():
    try:
        jobs = get_dynamodb_status()
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")

@app.route("/jobs", methods=["GET"])
def jobs():
    result = job_io.get_all_jobs()      # you currently return scan() response
    items = result.get("Items", [])     # extract items
    return jsonify(items), 200

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

@app.route("/status/<job_id>", methods=["GET"])
def status(job_id):
    item = job_io.get_job(job_id)
    if not item:
        return jsonify({"error": "not found"}), 404
    return jsonify(item), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

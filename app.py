"""
Flask + RQ — Day 1
Producer: receives HTTP requests and enqueues background jobs.
"""

from flask import Flask, jsonify
from redis import Redis
from rq import Queue

from jobs import count_words

app = Flask(__name__)

# --- infrastructure connections ---
redis_conn = Redis(host="localhost", port=6379)
q = Queue(connection=redis_conn)          # default queue named "default"


# ------------------------------------------------------------------
# /ping  — smoke-test that Flask is alive
# ------------------------------------------------------------------
@app.get("/ping")
def ping():
    return jsonify(status="ok", message="pong")


# ------------------------------------------------------------------
# /jobs  — enqueue a sample background job
# ------------------------------------------------------------------
@app.post("/jobs")
def create_job():
    text = "The quick brown fox jumps over the lazy dog"

    # enqueue returns a Job object immediately; the worker runs it later
    job = q.enqueue(count_words, text)

    return jsonify(
        job_id=job.id,
        status=job.get_status().value,   # "queued"
        queue_length=len(q),
    ), 202                               # 202 Accepted — work is pending


if __name__ == "__main__":
    app.run(debug=True)
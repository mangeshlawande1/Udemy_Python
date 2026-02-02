from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queue.worker import process_query


app = FastAPI()


@app.get('/')
def root():
    return {"status":"Server is up and running "}

@app.post('/chat')
def chat(
        query:str=Query(..., description="the chat query of user ")
):
    job = queue.enqueue(process_query, query)
    # it will take some time to process, returns id of jobs 
    #  gose into the line, 

    return { "status": "queued", "job_id":job.id }

@app.get("./job-status")
def get_result(
        job_id:str= Query(..., description="Job ID")

):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {"result":result }

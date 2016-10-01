from flask import Flask, request, Response
import json
import datetime
from FlowOptimizer import FlowOptimizer

app = Flask(__name__)


@app.route('/flow/api/v1/invert', methods=['POST'])
def flow():
    # Get json request
    request_json = request.json

    # Get parameters
    output_goal = request_json.get("requestedFlow")
    num_of_controls = request_json.get("numOfControls")
    floor = request_json.get("floor")
    ceiling = request_json.get("ceiling")
    headwater = request_json.get("headwater")
    tailwater = request_json.get("tailwater")
    timeseries_name = request_json.get("timeseriesName")

    # Get timestamp
    timestamp = request_json.get("timestamp")
    if timestamp is None:
        timestamp = now()

    # Create FlowOptimizer and get results
    flow_optimizer = FlowOptimizer(output_goal, num_of_controls, floor, ceiling)
    results = flow_optimizer.optimize(timestamp, headwater, tailwater, timeseries_name)

    # Calculate the output and create response
    actual_output = flow_optimizer.get_output(timestamp, headwater, tailwater, results, timeseries_name)
    response_data = {"expectedOutput": output_goal,
                     "actualOutput": actual_output,
                     "controlValues": results}

    # Convert and send response
    js = json.dumps(response_data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


def now():
    dt = datetime.datetime.now()
    return dt.isoformat()


if __name__ == '__main__':
    app.run()

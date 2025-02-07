This project is my submission to the Fetch backend challenge at:
https://github.com/fetch-rewards/receipt-processor-challenge 

My implementation was created using the Python Flask framework 
I use some libraries that may need to be installed when running locally:
from flask import Flask, jsonify, request
import uuid
import os
import math
import json

To run locally, pull this repo, navigate to the receipt-api folder and run "python processor.py" 
This implemention uses local storage in the receipts folder and stores jsons as <generated_id>.json
The two endpoints can be reached at:
http://localhost:5000/receipts/process

http://localhost:5000/receipts/{id}/points


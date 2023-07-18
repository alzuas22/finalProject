from flask import Flask, render_template
import requests

app = Flask(__name__)
app.config.from_prefixed_env()
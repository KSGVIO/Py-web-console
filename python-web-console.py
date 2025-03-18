from flask import Flask, render_template, request, Response
import subprocess

app = Flask(__name__)

def run_command(command):
    """Runs a command and streams output live to the frontend."""
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1, universal_newlines=True
    )

    for line in iter(process.stdout.readline, ""):
        yield line.strip() + "\n"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/execute", methods=["POST"])
def execute():
    """Execute command and stream output."""
    command = request.form.get("command")
    return Response(run_command(command), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

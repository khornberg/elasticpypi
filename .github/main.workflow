workflow "Build and Test" {
  on = "push"
  resolves = [ "Report", "Lint" ]
}

action "Curl" {
  uses = "actions/bin/curl@master"
  args = "curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter"
}

action "Prepare" {
  uses = "actions/bin/sh@master"
  args = ["chmod +x ./cc-test-reporter && ./cc-test-reporter before-build"]
  secrets = ["CC_TEST_REPORTER_ID"]
  needs = ["Curl"]
}

action "Build" {
  uses = "jefftriplett/python-actions@master"
  args = "pip install -r requirements.txt && pip install -r test-requirements.txt"
  needs = ["Prepare"]
}

action "Lint" {
  uses = "jefftriplett/python-actions@master"
  args = "flake8 --max-complexity=6 --max-line-length=120 --exclude node_modules,.requirements,venv"
  needs = ["Build"]
}

action "Test" {
  uses = "jefftriplett/python-actions@master"
  args = "python -m pytest --cov=elasticpypi --cov-report=term-missing --cov-report=xml"
  needs = ["Build"]
}

action "Report" {
  uses = "actions/bin/sh@master"
  args = ["apt-get update && apt-get install git-core -y && ./cc-test-reporter after-build --coverage-input-type coverage.py"]
  needs = ["Test"]
  secrets = ["CC_TEST_REPORTER_ID"]
}

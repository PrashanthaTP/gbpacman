import subprocess


def run_cmd(cmd: list, **kwargs):
    run_options = {
        "shell": False,
        "capture_output": True,
        "text": True
    }

    for key in kwargs:
        run_options[key] = kwargs[key]
    try:
        res = subprocess.run(cmd, **run_options)
        return res
    except subprocess.CalledProcessError as e:
        raise

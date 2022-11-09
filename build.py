import datetime
import pathlib
import shutil
import subprocess
import sys
import tempfile

THIS = pathlib.Path(__file__).resolve().parent
VENV = pathlib.Path(tempfile.mkdtemp(prefix="venv_", dir=THIS)).resolve()

subprocess.run([sys.executable, '-m', 'venv', VENV])

PYTHON = VENV / 'Scripts' / 'python.exe'
PIPARGS = [PYTHON, '-m', 'pip', 'install']
subprocess.run([*PIPARGS, '--upgrade', 'pip', 'wheel'])
subprocess.run([*PIPARGS, 'pyinstaller'])
subprocess.run([*PIPARGS, '-r', THIS / 'requirements.txt'])

DIST = THIS / f"dist-{datetime.datetime.now():%Y%m%d-%H%M%S}"
WORK = VENV / '__build'

PYINSTALLER = VENV / 'Scripts' / 'pyinstaller.exe'
PYINSTALLER_ARGS = [PYINSTALLER, '--distpath', DIST, '--workpath', WORK]

STREAMER = THIS / 'streamer.spec'
MODERATOR = THIS / 'moderator.spec'

subprocess.run([*PYINSTALLER_ARGS, STREAMER])
subprocess.run([*PYINSTALLER_ARGS, MODERATOR])


shutil.rmtree(VENV, ignore_errors=True)

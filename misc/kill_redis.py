# name is self-explanatory
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

# netstat -ano | findstr :6379
# for /f "tokens=5" %a in ('netstat -ano ^| findstr :6379') do taskkill /F /PID %a

port = os.getenv('REDIS_PORT')

result = subprocess.run(
    f"netstat -ano | findstr :{port}",
    shell=True,
    capture_output=True,
    encoding='cp866'
)
print("Before:")
print(result.stdout)

accept = input("Kill Redis? (y/n): ").strip().lower()
if accept != 'y':
    exit()

netstat_cmd = f'netstat -ano ^| findstr :{port}'
for_cmd_inner = f'\'{netstat_cmd}\''
full_cmd = f'for /f "tokens=5" %a in ({for_cmd_inner}) do taskkill /F /PID %a'

result = subprocess.run(
    full_cmd,
    shell=True,
    capture_output=True,
    encoding='cp866'
)


print("Result:")
print(result.stdout)
if result.stderr:
    print("Error:")
    print(result.stderr)

result = subprocess.run(
    f"netstat -ano | findstr :{port}",
    shell=True,
    capture_output=True,
    encoding='cp866'
)
print("After:")
print(result.stdout)

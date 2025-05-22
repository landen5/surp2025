# surp2025

activate virtual environment:
. .venv/bin/activate 

start flask server:
cd backend
python3 main.py

start react:
cd my-app
npx expo start
a

connect to ec2
ssh -i datasurpkey.pem ec2-user@ec2-13-57-205-80.us-west-1.compute.amazonaws.com
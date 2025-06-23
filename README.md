# surp2025

activate virtual environment:
source .venv/bin/activate 

start flask server:
cd backend
python3 main.py

start react:
cd my-app
npx expo run:android
a

connect to ec2 and run flask:
ssh -i datasurpkey.pem ec2-user@ec2-13-57-205-80.us-west-1.compute.amazonaws.com
cd surp2025
source venv/bin/activate
cd backend
python3 main.py
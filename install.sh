sudo apt-get update 
sudo apt-get install python3 python3-venv

mkdir ~/jira-evaluation
cd ~/jira-evaluation

python3 -m venv jira_python
source jira_python/bin/activate
pip install 'jira[cli]' flask python-dotenv
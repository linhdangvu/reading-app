Installing env Python
`virtualenv .env`
`source .env/bin/activate`

pip install -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development
flask run

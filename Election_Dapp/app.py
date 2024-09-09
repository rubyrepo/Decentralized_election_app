from flask import Flask, render_template, request
from voting_deploy_part_01 import abi,bytecode, chain_id, w3
from Keys import my_address,private_key
from data import OTP, Voted_OTP, db
from voting_deploy_part_02 import DEPLOY, VIEWVOTESTATUS, PLACEVOTE,DEPLOY_ONCE

app = Flask(__name__)

tx_receipt = None
nonce = None
election = None
contract_address = None
flag = True

DEPLOY_ONCE()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    name = request.form.get('textinput')
    otp = request.form.get('otpinput')
    otp = int(otp)
    vote = request.form.get('vote')
    vote = int(vote)
    print(f"This is the name: {name}")
    print(f'This is the otp: {otp}')
    print(f"This is the vote: {vote}")


    if otp in OTP and otp not in Voted_OTP:
        Voted_OTP.append(otp)
        PLACEVOTE(vote)
        vote_status = VIEWVOTESTATUS()
        vote_status  = list(vote_status)
        awl = vote_status[0]
        bnp = vote_status[1]
        neutral = vote_status[2]
        total = vote_status[3]
        return render_template('statusview.html',awl=awl,bnp=bnp,neutral=neutral,total=total)

    else:
        vote_status = VIEWVOTESTATUS()
        vote_status = list(vote_status)
        awl = vote_status[0]
        bnp = vote_status[1]
        neutral = vote_status[2]
        total = vote_status[3]
        return render_template('unsuccessful.html', awl=awl, bnp=bnp, neutral=neutral, total=total)


if __name__ == '__main__':
    app.run(debug=True)
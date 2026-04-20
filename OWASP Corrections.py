from flask import flask, jsonify
from flask_login import login_required, current_user

#Please note: While I am familiar with Python, I have not really used Java/Javascript before. My fixes for those codes are dependent on if I could find something online that pointed me in the right direction or provided examples I could use. 
#I'm also using VSCode which is throwing errors on everything for Java/Javascript and even on Python (for libararies I haven't installed) so I'm not sure if something is actually in a workable state or not.


##Broken Access Control

#1
#There is an issue with authentication here, but I am not sure how to fix it. I looked up a few javascript authentication issues but could not find one that matched this case. Adding a few things, but not sure how to bring it together. 
app.get('/profile/:userId', authenticate, (req, res) => {
    User.findById(req.params.userId, (err, user) => {
        if (err) return res.status(500).send(err);
        res.json(user);
    });
});

#2
#Any user could access the account. Added a login requirement and checking to make sure the user id matches. If not, it throws an error. 
@app.route('/account/<user_id>')
@login_required
def get_account(user_id):
    if current_user.id != user_id:
        return jsonify({'error': 'Forbidden'}), 403
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


## Cryptographic Failures

#3 
#MD5 is too fast for passwords and is easily breakable. Changing to bcrypt and updating hashing script (not sure how to fix it as-is, so changing it entirely)

import org.mindrot.jbcrypt.BCrypt;

String hashed = BCrypt.hashpw(password, Bcrypt.gensalt());
string hashed = Bcrypt.hashpw(password, BCrypt.gensalt(12));

if (BCrypt.checkpw(candidate, hashed)):
    System.out.println("Matches");
else:
    System.out.println("Does not match");


#4
#changed it from hashlib SHA1 to bcrypt because hashlib is too fast for passwords and is easily breakable
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


## Injection

#5
#The username is directly pulled from the URL which means a command can be entered as a username to manipulate the database. Adding prepared statements helps this.
String username = request.getParameter("username");
String query = "SELECT * FROM users WHERE username = ?";
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, username);
ResultSet rs = stmt.executeQuery();


#6
#The issue is similar to #5 in that the inputted information can be used to "hack" the system and display information. We need to scrub the input. I've added mongoSanitize to clean the input
const mongoSanitize = require('express-mongo-sanitize');
const express = require('express');
const app = express();

app.use(mongoSanitize());

app.get('/user', (req, res) => {
    // Directly trusting query parameters can lead to NoSQL injection
    db.collection('users').findOne({ username: req.query.username }, (err, user) => {
        if (err) throw err;
        res.json(user);
    });
});


##Insecure Design
#7
#Design flaws here are that it does not verify the user or hash the password. Adding password hashing. From what I found about identity verification, it's common to use tokens, but I am not sure how that works. Didn't add it in here, wasn't sure how.
import bcrypt

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']
    new_password = request.form['new_password']
    user = User.query.filter_by(email=email).first()
    if not user:
        return 'User not found', 404
    user.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    db.session.commit()
    return 'Password reset'



##Software and Data Integrity Failures
#8
#Honestly not sure where to begin with this one. I can see its an HTML tag, but I don't know why it's considered insecure
<script src="https://cdn.example.com/lib.js"></script>

## Server-Side Request Forgery
#9
#The issue is that this just pulls and prints the URL without any sort of scrubbing or verification. It could be used to access confidential information by entering an IP address. 

from urllib.parse import urlparse
import requests

ALLOWED_HOSTS = {"ivytech.edu", "battle.net"}

url = input("Enter URL: ")
if urlparse(url).hostname in ALLOWED_HOSTS:
    print(requests.get(url, timeout=5).text)
else:
    print("URL not allowed")

## Identifcation and Authentication Failures
#10
#Passwords should be encrypted, this is not. Adding encryption
if (BCrypt.checkpw(inputPassword, user.getPassword())) { 
    // Login success
}
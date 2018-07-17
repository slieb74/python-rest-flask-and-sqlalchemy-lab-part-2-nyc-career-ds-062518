# imported Flask and jsonify from flask
# imported SQLAlchemy from flask_sqlalchemy
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

# initialized new flask app
app = Flask(__name__)
# added configurations and database
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# connected flask_sqlalchemy to the configured flask app
db = SQLAlchemy(app)

# created models for application
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    tweets = db.relationship('Tweet', backref='users', lazy=True)
    def to_dict(self):
        user = {'id': self.id, 'username': self.username, 'tweets': [tweet.to_dict() for tweet in self.tweets]}
        return user

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates="tweets")
    def to_dict(self):
        tweet = {'id': self.id, 'text': self.text, 'user_id': self.user.id, 'user': self.user.username}
        return tweet


# DEFINE ROUTES THAT RETURN APPROPRIATE HTML TEMPLATES HERE
@app.route('/users')
def users():
    users_dict = [user.to_dict() for user in User.query.all()]
    return render_template('users.html',users = users_dict)

@app.route('/users/<int:id>')
def user_id(id):
    users_dict = [user.to_dict() for user in User.query.all() if user.id == id][0]
    return render_template('user_show.html', user=users_dict)

@app.route('/users/<username>')
def username(username):
    users_dict = [user.to_dict() for user in User.query.all() if user.username.lower()==username.lower()][0]
    return render_template('user_show.html', user=users_dict)

@app.route('/tweets')
def tweets():
    tweets_dict = [tweet.to_dict() for tweet in Tweet.query.all()]
    return render_template('tweets.html',tweets = tweets_dict)

@app.route('/tweets/<int:id>')
def tweet_id(id):
    tweets_dict = [tweet.to_dict() for tweet in Tweet.query.all() if tweet.id ==id][0]
    return render_template('tweet_show.html',tweet = tweets_dict)

#Tweets that belong to a user by user_id
@app.route('/users/<int:id>/tweets')
def tweets_user_id(id):
    users_dict = [user.to_dict() for user in User.query.all() if user.id==id][0]
    return render_template('tweets.html', tweets=users_dict['tweets'])

#Tweets that belong to a user by a user's name
@app.route('/users/<username>/tweets')
def tweets_username(username):
    users_dict = [user.to_dict() for user in User.query.all() if user.username.lower()==username.lower()][0]
    return render_template('tweets.html', tweets=users_dict['tweets'])

#A single User that is associated to a tweet by its id
@app.route('/tweets/<int:id>/user')
def user_tweet_id(id):
    tweet_with_id = [tweet.to_dict() for tweet in Tweet.query.all() if tweet.id ==id][0]
    user_id = tweet_with_id['user_id']
    user_with_tweet = [user.to_dict() for user in User.query.all() if user.id == user_id][0]
    return render_template('user_show.html', user=user_with_tweet)

# run flask application
if __name__ == "__main__":
    app.run()

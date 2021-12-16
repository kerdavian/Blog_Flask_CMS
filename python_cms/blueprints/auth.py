from flask import Blueprint, redirect, request, url_for
from flask_login import login_user, login_required, logout_user
import json
import requests
from oauthlib.oauth2 import WebApplicationClient
from os import environ
from python_cms.models.user import UserModel

# Oauth Configuration
GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration")

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login")
def login():
  # Find out what URL to hit for Google login
  google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
  authorization_endpoint = google_provider_cfg["authorization_endpoint"]

  # construct the request for Google login and provide
  # scopes that let you retrieve user's profile from Google
  request_uri = client.prepare_request_uri(
      authorization_endpoint,
      redirect_uri=request.host_url + "authorize",
      scope=["openid", "email", "profile"],
  )
  return redirect(request_uri)


@auth_blueprint.route("/authorize")
def authorize():
  # Get authorization code Google sent back to you
  code = request.args.get("code")

  # Find out what URL to hit to get tokens that allow you to ask for
  # things on behalf of a user
  google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
  token_endpoint = google_provider_cfg["token_endpoint"]

  # Prepare and send request to get tokens!
  token_url, headers, body = client.prepare_token_request(
      token_endpoint,
      authorization_response=request.url,
      redirect_url=request.base_url,
      code=code,
  )
  # send the request to get the tokens
  token_response = requests.post(
      token_url,
      headers=headers,
      data=body,
      auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
  )

  # Parse the tokens from the response body
  client.parse_request_body_response(json.dumps(token_response.json()))

  # Now that we have tokens let's find and hit the URL
  # from Google that gives the user's profile information,
  # including their Google Profile Image and Email
  userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
  uri, headers, body = client.add_token(userinfo_endpoint)
  userinfo_response = requests.get(uri, headers=headers, data=body)

  # We want to make sure their email is verified.
  # The user authenticated with Google, authorized our
  # app, and now we've verified their email through Google!
  print(userinfo_response.json())
  if userinfo_response.json().get("email_verified"):
    unique_id = userinfo_response.json()["sub"]
    users_email = userinfo_response.json()["email"]
    picture = userinfo_response.json()["picture"]
    users_name = f'{userinfo_response.json()["family_name"]} {userinfo_response.json()["given_name"]}'
  else:
    return "User email not available or not verified by Google.", 400

  # Create a user in our database with the information provided
  # by Google
  user = UserModel(id=unique_id,
                   name=users_name,
                   email=users_email,
                   picture=picture)

  # Doesn't exist? Add to database
  if not UserModel.get(unique_id):
    user.save()

  # Begin the user session by logging the user in.
  # user should be an instance of your `User` class
  login_user(user)

  # redirect the user back to homepage
  return redirect(url_for("pages.index"))


@auth_blueprint.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("pages.index"))

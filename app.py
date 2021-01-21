import json

from flask import Flask, render_template, g, redirect, url_for, request
from flask_oidc import OpenIDConnect
from okta import UsersClient
import requests

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "{{ LONG_RANDOM_STRING }}"
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
okta_client = UsersClient("https://dev-7675953.okta.com", "00e6WXulRPyd_QYxZpMwnLeaUQPATENvtZv4UIkdjv")
api_headers = {
            'authorization': 'SSWS 00e6WXulRPyd_QYxZpMwnLeaUQPATENvtZv4UIkdjv',
            'accept': 'application/json',
            'content-Type': 'application/json'
        }
USER_API_ENDPOINT = "https://dev-7675953.okta.com/api/v1/users"
GROUPS_API_ENDPOINT = "https://dev-7675953.okta.com/api/v1/groups"
ADMIN_GROUP_ID = "00g3xcq8jCzdmFziW5d6"

@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")

@app.route("/admin_dashboard")
@oidc.require_login
def admin_dashboard():
    if not g.user:
        return {"response": "Please log in as Admin to access this page"}
    me_id = g.user.id
    group_ids = list_group_ids_for_user(me_id)
    is_admin = ADMIN_GROUP_ID in group_ids
    if is_admin:
        return render_template("admin_dashboard.html")
    else:
        return {"response": "Current user is not an admin"}


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/list_users")
def list_users():
    response = requests.get(USER_API_ENDPOINT, headers=api_headers)
    users = json.loads(response.content)
    return { "response": users}


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    response = requests.delete(USER_API_ENDPOINT + "/" + user_id, headers=api_headers)

    if response.status_code >= 400:
        return {"response": "Tried deleting user " + user_id + " but FAILED!"}
    else:
        return {"response": "Deleting user " + user_id + " SUCCESS!"}

@app.route("/read_user/<user_id>")
def read_user(user_id):
    response = requests.get(USER_API_ENDPOINT + "/" + user_id, headers=api_headers)

    if response.status_code >= 400:
        return {"response": "Tried reading user " + user_id + " but FAILED!"}
    else:
        return {"response": json.loads(response.content)}

@app.route("/list_groups")
def list_groups():
    response = requests.get(GROUPS_API_ENDPOINT, headers=api_headers)
    groups = json.loads(response.content)
    return {"response": groups}

@app.route("/make_admin/<user_id>")
def make_admin(user_id):
    response = requests.put(GROUPS_API_ENDPOINT + "/" + ADMIN_GROUP_ID + "/users/" + user_id, headers=api_headers)

    if response.status_code >= 400:
        return {"response": "Tried making admin " + user_id + " but FAILED!"}
    else:
        return {"response": "Tried making admin " + user_id + " SUCCESS!"}


def list_group_ids_for_user(user_id):
    response = requests.get(USER_API_ENDPOINT + "/" + user_id + "/groups", headers=api_headers)
    user_groups = json.loads(response.content)
    return map(lambda user_group: user_group["id"], user_groups)


@app.route("/create_user")
def create_user():
    # create user with custom attribute
    body = {
            "profile": {
            "firstName": request.args.get('firstName') or "John",
            "lastName": request.args.get('lastName') or "Doe",
            "email": request.args.get("email"),
            "login": request.args.get("email"),
            "mobilePhone": request.args.get("mobilePhone"),
        }
    }
    response = requests.post(
        USER_API_ENDPOINT + "?activate=false",
        headers=api_headers,
        data=json.dumps(body)
    )

    return {"response": json.loads(response.content)}

@app.route("/update_user/<user_id>")
def update_user(user_id):
    body = {
        "profile": request.args
    }
    response = requests.post(
        USER_API_ENDPOINT + "/" + user_id,
        headers=api_headers,
        data=json.dumps(body)
    )

    return {"response": json.loads(response.content)}


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))
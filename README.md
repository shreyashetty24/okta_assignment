Technical Exercise

Note : Referred developer blog post for building Flask web app using OpenID Connect and Okta. 
https://developer.okta.com/blog/2018/07/12/flask-tutorial-simple-user-registration-and-login

This will install all the project dependencies,
pip install -r requirements.txt

1. An unsecured (“open”) landing page 
Visit http://localhost:5000 

2. A protected page that any authenticated user can get to
In order to launch the protected page, log onto the URL "http://localhost:5000/dashboard". The user is redirected to the hosted sign-in page (https://dev-7675953.okta.com/) where the user can authenticate. After successful authentication, the browser is redirected back to the application along with information about the user.
   

3. A protected page that only members of an admin group can get to
https://github.com/shreyashetty24/okta_assignment/blob/cdb536944ca59c3394aff1ed3b6e8c585b3bb48d/app.py#L44
When you launch the app, click on Admin Dashboard on top right corner. Only user part of the admin group has access to this page
If not an admin, it will return a response of Current user is not an admin. 
   
4. An admin page that provides an interface to add regular users to the admin group
https://github.com/shreyashetty24/okta_assignment/blob/cdb536944ca59c3394aff1ed3b6e8c585b3bb48d/app.py#L93
Did not create Admin UI, instead used the Okta API to add regular users(using their UserID) to the admin group

5. Create custom admin pages that use the Okta API for Create, Read, Update, & Delete user functions. 

Create :
https://github.com/shreyashetty24/okta_assignment/blob/cdb536944ca59c3394aff1ed3b6e8c585b3bb48d/app.py#L109
Did not create Admin UI, instead made API calls to get the response. 
Example : Using the bellow URL (protocol, server URL, path, query parameters) you can create a new user. 
http://localhost:5000/create_user?email=shreya.shetty6@sample.com&firstName=Shay&lastName=Shetty

Read : 
https://github.com/shreyashetty24/okta_assignment/blob/cdb536944ca59c3394aff1ed3b6e8c585b3bb48d/app.py#L78
Did not create Admin UI, instead made API calls to get the response.
Example : Using this URL (http://localhost:5000/read_user/00u42r0x4kU8YfzHt5d6) you can get the profile of that specific user 

Update :
https://github.com/shreyashetty24/okta_assignment/blob/cdb536944ca59c3394aff1ed3b6e8c585b3bb48d/app.py#L129
Did not create Admin UI, instead made API calls to get the response. 
Example : Using this URL (http://localhost:5000/update_user/00u42wjsjR8Y51Qgn5d6?firstName=Sony) you can update any argument within the profile (firstname in our example) 
Updated current user's profile using partial update

Delete :
https://github.com/shreyashetty24/okta_assignment/blob/cdb536944ca59c3394aff1ed3b6e8c585b3bb48d/app.py#L69
Did not create Admin UI, instead made API calls to get the response. 
Example : Using this URL (http://localhost:5000/delete_user/00u40x9ga4VpR3UUb5d6) you can delete the user permanently using their user ID.

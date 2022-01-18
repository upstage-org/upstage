from config.settings import EMAIL_HOST_USER

footer = """<br>
<br>
Thank you,
<br>
<i style="color: #007011">The Upstage Team!</i>
</p>
"""

def display_user(user):
    return user.display_name if user.display_name else user.username

def password_reset(user, otp):
    return f"""
<p>
Hi <b>{display_user(user)}</b>,
<br>
<br>
We received a request to reset your forgotten password. Please use the following code to proceed your password reset:
<b style="color: #007011">{otp}</b>
<br>
The code will expire in 30 minutes.
<br>
<br>
If you did not request a password reset, please ignore this email.
{footer}
"""

def user_registration(user):
    return f"""
<p>
Hi <b>{display_user(user)}</b>,
<br>
<br>
We are glad that your're here! Your account has been created and waiting for approval! You will receive an email once your account has been approved.
<br>
<br>
If you have any questions, please contact us at <a href="mailto:{EMAIL_HOST_USER}">{EMAIL_HOST_USER}</a>.
{footer}
"""

def user_approved(user):
    return f"""
<p>
Hi <b>{display_user(user)}</b>,
<br>
<br>
Thank you for registering with us. Your account has been approved! You can now login to the Upstage platform.
<br>
<br>
Here is your account information:
<br>
<br>
<b>Username:</b> {user.username}
<br>
<b>Password:</b> <i>the one you used to register</i>. If you forgot your password, click on the "Forgot Password" link on the login page.
{footer}
"""

def admin_registration_notification(user):
    return f"""
<p>
Dear Admins,
<br>
<br>
A new user has registered with the Upstage platform. Please approve the user by clicking on the following link:
<br>
<br>
<a href="{user.approval_url}">{user.approval_url}</a>
<br>
<br>
The user's information is:
<br>
<br>
<b>Username:</b> {user.username}
<br>
<b>Email:</b> {user.email}
<br>
<b>Display Name:</b> {user.display_name}
<br>
<br>
{footer}
"""
from config import EMAIL_HOST_USER

footer = """<br>
<br>
Thank you,
<br>
<b style="color: #007011">The UpStage Team!</b>
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
We are glad that you're here! Your account has been created and waiting for approval by an UpStage Admin. You will receive an email once your account has been approved.
<br>
<br>
Please look at the <a href="https://docs.upstage.live/">UpStage User Manual</a> for documentation on how to use UpStage.
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
Thank you for registering with us. Your account has been approved! You can now login to UpStage.
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


def admin_registration_notification(user, approval_url):
    return f"""
<p>
Dear Admins,
<br>
<br>
A new user has registered with UpStage. Please approve the user by clicking on the following link:
<br>
<br>
<a href="{approval_url}">{approval_url}</a>
<br>
<br>
The user's information is:
<br>
<br>
<b>Username:</b> {user.username}
<br>
<b>Full Name:</b> {user.first_name} {user.last_name}
<br>
<b>Email:</b> {user.email}
<br>
<b>Introduction:</b> {user.intro}
{footer}
"""


def request_permission_for_media(user, media, note, studio_url):
    return f"""
<p>
Hi <b>{display_user(media.owner)}</b>,
<br>
<br>
{display_user(user)} has requested permission to use your media <b>{media.name}</b>. Please go to the <a href="{studio_url}">Studio</a> and click on the Notification icon to approve or deny the request.
<br>
Purpose: {note}
<br>
<br>
{footer}
"""


def waiting_request_media_approve(user, media):
    return f"""
<p>
Hi <b>{display_user(user)}</b>,
<br>
<br>
Your permission request for media <b>{media.name}</b> has been sent to the owner, please wait to approve.
<br>
<br>
{footer}
"""


def request_permission_acknowledgement(user, media, note):
    return f"""
<p>
Hi <b>{display_user(media.owner)}</b>,
<br>
<br>
{display_user(user)} has indicated that they wish to use your media <b>{media.name}</b> and will acknoweldege it as you have specified.
<br>
<br>
Additional notes: {note}
<br>
<br>
{footer}    
"""


def permission_response_for_media(user, media, note, approved, studio_url):
    return f"""
<p>
Hi <b>{display_user(user)}</b>,
<br>
<br>
Your permission request for <b>{media.name}</b> with purpose \"{note}\" has been {'approved' if approved else 'denied'} by the owner.
{f'<br><br>You can now use the media in the <a href="{studio_url}">Studio</a>.' if approved else ''}
<br>
<br>
{footer}
"""

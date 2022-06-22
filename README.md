# Voting App - Django [Python]

- User model with registration implemented. User Registration, user Account Activation, Login and Logout are developed by Class-based views.
- When a user is registered, the user is prompted for a username, first_name, last_name, email and password. A prerequisite for registration is confirmation of email. A one-time link to activate your account is sent to your email.
- Implemented the ability for each user to view their Profile information and Edit the user Profile. Also, it is possible for the user to Delete his Profile.
- Each user has the opportunity to change his password in his personal Profile.
- Also implements login through social networks such as GitHub, Google and Instagram.
- Only registered users who have confirmed their email and users logged in through social networks can vote.
- Each user can only vote once per poll.
- Implemented a Contact form for feedback. If the User is authorized - one window is available to him - for the Message Text, his username and his email are taken from the request. If the user is anonymous, he needs to enter the required fields - Name, Email and Message Text.


__Used tools:__    
:heavy_check_mark: Python    
:heavy_check_mark: Django [web framework]   
:heavy_check_mark: Social auth app django    
:heavy_check_mark: HTML+CSS+Bootstrap    
:heavy_check_mark: SQLite database    
:heavy_check_mark: django-utils-six 2.0       

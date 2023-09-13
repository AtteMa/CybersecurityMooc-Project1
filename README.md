# Cyber Security Base course project 1

This is the course project 1 containing a csrf flaw and four flaws from the [OWASP top ten 2021](https://owasp.org/www-project-top-ten/)

Link to the repository: https://github.com/AtteMa/CybersecurityMooc-Project1

You can test the demo project by downloading and extracting the files and running the following commands:

```
pyhton manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

After successfully launched, you can find the demo project at [](http://127.0.0.1:8000/polls/)

# Flaw 1: Cross-site Request Forgery

Links to the flaws:
- https://github.com/AtteMa/CybersecurityMooc-Project1/blob/02002546115576e57cf397255818857114fdfd02/Cybersecurity-Project/polls/templates/polls/add_poll.html#L9
- https://github.com/AtteMa/CybersecurityMooc-Project1/blob/02002546115576e57cf397255818857114fdfd02/Cybersecurity-Project/polls/templates/polls/detail.html#L10

Cross-Site Request Forgery is a type of security vulnerability that occurs when a malicious website tricks a user's web browser into performing actions on a different website without their knowledge or consent. CSRF attacks exploit the trust that websites have in a user's browser. When a user is logged into any website, their browser stores authentication cookies that are automatically sent with future requests to that site. For example, an attacker can create a website containing malicious POST requests to the target website, using the legitimate users stored cookies to make it appear as if the user sent the request. To prevent CSRF attacks, websites use CSRF tokens. These tokens are unique for each user session and must be included with any request that changes data on the site. The server verifies the tokens authenticity, ensuring the request is legitimate and not generated by a malicious website.

Django has a built-in CSRF token functionality. To fix this issue, we need to remove the comments from {% csrf_token %} line in every form in our application and django will handle the rest.

# Flaw 2: SQL Injection

Links to the flaws:
- https://github.com/AtteMa/CybersecurityMooc-Project1/blob/baf7c0b449e7d22f00da336028c9df7409286a77/Cybersecurity-Project/polls/views.py#L41
- https://github.com/AtteMa/CybersecurityMooc-Project1/blob/baf7c0b449e7d22f00da336028c9df7409286a77/Cybersecurity-Project/polls/views.py#L68

Injection in general is a vulnerability in the application, where it is possible for a malicious user to send code to the server hidden as regular user data. The malicious code then gets executed on the server, and as an unexpedted action can cause all kinds havoc, from stolen user data to the deletion of whole databases. The most common form of injection is SQL injection, where the attacker tries to insert malicious SQL code inside the input or parameter fields of the legitimate SQL query. To prevent SQL injections, one needs to properly parameterize their queries and validate and sanitize their input data, so that the query does not contain anything extra.

In the code, the injection is already fixed with djangos "models" framework. Models provides tools for sanitizing and parametrizing database queries. Using models in the application prevents injection to the SQLite database. The commented lines of the code contain the flawed implementation, in which we use direct database connection with an SQL query vulnerable to injection.

# Flaw 3: Insecure Design

Links to the flaws:
- https://github.com/AtteMa/CybersecurityMooc-Project1/blob/f9a9d4b8bb6d798cdda07168d2939e2b2fd3a133/Cybersecurity-Project/polls/tests.py#L1
- https://github.com/AtteMa/CybersecurityMooc-Project1/blob/3545c791edea7598c37f428e58db90c443ae6d4e/Cybersecurity-Project/polls/views.py#L10

Insecure design refers to the creation of software systems, applications, or products that inherently lack the necessary security measures to protect against potential threats and vulnerabilities. It is different from insecure implementation, in which one can have flaws in the software implementation despite having a secure design. Insecure implementation can always be fixed with the tools that well thought out secure design provides, but insecure design cannot be fixed by even a perfect implementation as by definition, needed security controls were never created in the first place.

The lack of unit or integration testing is inherently insecure design. The flaw in my project is the complete lack any testing. This can be fixed creating a wide range of automated tests with the tools django provides. One should also build the application from the ground up using TDD, Test Driven Development. In the code there are commented-out automated tests to test the core functionalities of the application. We can also add logging so it will be easier to track and identify possible vulnerabilities or defects.

# Flaw 4: Vulnerable and Outdated Components

Links to the flaws:

Vulnerable and outdated components is a flaw where the software is built using pre-existing components, for example older versions of libraries and dependancies that have known vulnerabilites, thereby exposing the application to these vulnerabilities as well. To counter this flaw, the developer must regularly audit the versions of any frameworks or components their application uses. In this application we are using django, which luckily notifys us automatically when there is a new version available. Django also has automatic warnings for outdated dependencies.

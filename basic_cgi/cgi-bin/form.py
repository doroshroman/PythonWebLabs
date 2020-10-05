#!/usr/bin/env python3
import cgi
import html
import os
import http.cookies

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
visitor_counter = cookie.get("counter").value
visitor_counter = int(visitor_counter) + 1 if visitor_counter else 0
print(f"Set-Cookie: counter={visitor_counter}")

form = cgi.FieldStorage()
not_found = 'not found'
name = html.escape(form.getvalue('name', not_found))
surname = html.escape(form.getvalue('surname', not_found))
interests = form.getvalue('interest', not_found)
age = form.getvalue('age', not_found)

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Form processing</title>
        </head>
        <body>""")

print("<h2>Thank you for your reply!</h2>")
print("<h3>Your results:</h3>")
print(f"<p>Name: {name}</p>")
print(f"<p>Surname: {surname}</p>")
print(f"<p>Interests: {','.join(interests) if interests != not_found else not_found}</p>")
print(f"<p>Age: {age}</p>")
print("""</body>
        </html>""")
        
print(f"This form was submitted by: {visitor_counter}")
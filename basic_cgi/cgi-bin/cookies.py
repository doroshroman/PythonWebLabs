#!/usr/bin/env python3
import os
import http.cookies

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
visitor_counter = cookie.get("counter").value
visitor_counter = int(visitor_counter) + 1 if visitor_counter else 0
print(f"Set-Cookie: counter={visitor_counter}")
print("Content-Type: text/html\n")

print(f"This form was submitted by: {visitor_counter}")

#!/usr/bin/env python3
import os
import http.cookies

cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
visitor_counter = cookie.get("counter") 
if visitor_counter is None:
    print("Set-cookie: counter=1; expires=Wed May 18 03:33:20 2033; path=/cgi-bin/; httponly")
    print("Content-type: text/html\n")
    print("There is no cookie yet!")
else:
    print("Content-type: text/html\n")
    print("Cookies:")
    print(visitor_counter.value)
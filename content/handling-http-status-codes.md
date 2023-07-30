Title: Handling HTTP Status Codes
Date: 2023-07-30 13:27
Category: web
Tags: web, python, restful


# Introduction

Error handling has been an unglamorous, undervalued, and essential part of
protocols and interfaces since time immemorial.

As any critical design choice, there are many flavours: return values, as in C
and Go; exceptions, as in Java and Python; or much better alternatives, as in
Haskell and Rust.

HTTP, being a request-response network protocol, is limited to return values.

# Error Handling with Return Values

C and Go have a slight design difference. In C, error handling is not part of
the language. The programmer could choose to handle errors in any of a number
of ways. This creative freedom resulted in countless terrible choices and
some inspired interfaces.

Decades later, the designers of Go recognised that this freedom is not worth
the cognitive cost, nor the terrible mistakes. Go clearly favours very
explicit return value error codes. Love it or hate it, this uniformity has
value in itself.

Both C and Go error codes have something in common, there is one value which
represents success, and many values to describe failure. This characteristic
is not limited to programming languages, POSIX processes are the same. This
asymmetry between success and failure appears in almost every instance. One
exception is HTTP.

# HTTP Status Codes

Being a network protocol, one goal of HTTP is to avoid being "chatty". This
means that every interaction should request substantial amount of work, and
respond in a way that your application can continue without further interaction,
for the given action.

For requests, this is solved by resources representing application level
concepts and verb representing high level operations.

For responses, this is solved by having granularity on the status codes. The 
standard includes 39 status codes to represent failure, and 10 to represent
success. Does this mean every response handler should have at least 49 cases?
Fortunately, HTTP has an additional sophistication to handle this complexity.

HTTP defines a hierarchy for status codes. Codes between 100 and 199 are
"informational", between 200 and 299 mean some form of success, between 300 and
399 mean that some the client needs to perform some additional action, between
400 and 499 mean that the client made some mistake and between 500 and 599
that there was some problem on the server.

This means that the simplest client needs to handle 5 cases! Most HTTP
libraries will handle 1xx and 3xx status codes, so application code needs to
worry about only 3, according to my calculations.

Nevertheless, this does not mean that all those 49 codes are actually useless,
depending on the actual application, those codes could be in use and the
client might need to handle them specifically.

# How to Handle HTTP Status Codes

This brings us to the recommendation:

- Use an HTTP library which handles standard 1xx and 3xx codes.
- Every HTTP client should handle the 2 failure status code families
  in a generic way.
    - Declare a programming error in case of a 4xx.
    - Retry a few times after a delay for a 5xx, and then give up.
- Handle specific codes for standard functionality you are using. For example,
  if your application uses authentication, handle 401; if your application
  uses rate-limiting, handle 429.
- If the application defines custom codes, handle those. For example, 530
  "Site is frozen" should not be retried.
- Handle any custom code outside of the standard families.

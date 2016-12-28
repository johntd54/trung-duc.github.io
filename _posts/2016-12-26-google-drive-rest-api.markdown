---
layout: post
title: "161226 - Google Drive REST API"
date: 2016-12-26 02:53:04
categories: GoogleAppEngine
---

# Drive REST API capabilities

- Download, upload files
- Create and open files from Google Drive web UI
- Searches for files
- Share and collaborate
- Use shortcuts
- Export and convert Google Docs

# Google API Authentication and Authorization
(focus mainly in installed apps)

## Overview

App developers gets OAuth2.0 credentials for their client app from Google Api Console ----> App developers embed the credientials inside the source code of their client app ---> During usage, client app uses that credentials to request access token from Google server ----> (if authorized) Google server sends back access token to client app ----> Client app uses that access token for the Google API that it is registered.

## Little more detail

1. Obtain OAuth 2.0 credentials from Google API console. This step is to establish a connection between your app and Google, through the mutually known client ID and client secret

2. Obtain access token from Google Authorization Server. APIs typically are not there for everyone to freely access. The application must request and get an access token to use the APIs. Some types of requests require users to log in and explicitly allow permissions that your app request. This is called user consent.

3. Send access token to use API.

4. Refresh the access token if necessary, using refresh token.

## Token expirations

When:

- Users revoke access from the app
- Token has not been used for 6 months
- User changed password and the token contain Gmail scopes
- User account exceeds a certain number of tokens requests

## Note:

- The client ID and secret ID should be embedded inside client app's source code, which ironically makes it not a secret... 
- (From some testing with Google Drive Python API)
 + the access token json file must contains all original keys (regardless of values)
 + as long as access_token is still valid (has not expired), the value of refresh_token, client_id and client_secret are unnecessary

# Resources

- [Python API Client Library](https://developers.google.com/api-client-library/python/guide/aaa_oauth)


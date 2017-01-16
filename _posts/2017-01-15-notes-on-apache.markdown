---
layout: post
title: "170115 - Notes on Apache"
date: 2017-01-15 22:11:34
categories: apache note
---

# Overview

- it is a piece of software that runs in the background (hence it's best that the system supports multi-tasking)
- its main purpose is to listen to request (from IP addresses specified inside its config files), analyzes that request, and returns a response
- it can be extended by modules
- it is set up to run through its configuration files
- multiple domains can be on the same IP (virtual hosts), or vice versa (multiple servers or multi-addresses)

    + in the first case, the process looks as follow: user types domain name -> browser sends the domain name to DNS service -> DNS service returns the IP address of that domain name -> browser connects to that IP address, with the domain name in HOST header to let server know which site should be served if the server hosts multiple sites
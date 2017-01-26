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


# Virtual hosts
(the text below is the most important partially copied from [here](https://httpd.apache.org/docs/2.4/vhosts/details.html))

- There is a main server which consists of all the definitions appearing outside of <VirtualHost> sections.
- There are virtual servers, called vhosts, which are defined by <VirtualHost> sections.
- Each VirtualHost directive includes one or more addresses and optional ports. Hostnames can be used in place of IP addresses in a virtual host definition, but they are resolved at startup and if any name resolutions fail, those virtual host definitions are ignored. This is, therefore, not recommended. The address can be specified as *, which will match a request if no other vhost has the explicit address on which the request was received. The address appearing in the VirtualHost directive can have an optional port. If the port is unspecified, it is treated as a wildcard port, which can also be indicated explicitly using *. The wildcard port matches any port. Collectively the entire set of addresses (including multiple results from DNS lookups) are called the vhost's address set.
- Apache automatically discriminates on the basis of the HTTP Host header supplied by the client whenever the most specific match for an IP address and port combination is listed in multiple virtual hosts.
- The ServerName directive may appear anywhere within the definition of a server. However, each appearance overrides the previous appearance (within that server). If no ServerName is specified, the server attempts to deduce it from the server's IP address. The first name-based vhost in the configuration file for a given IP:port pair is significant because it is used for all requests received on that address and port for which no other vhost for that IP:port pair has a matching ServerName or ServerAlias. It is also used for all SSL connections if the server does not support Server Name Indication.
- If a vhost has no ServerAdmin, Timeout, KeepAliveTimeout, KeepAlive, MaxKeepAliveRequests, ReceiveBufferSize, or SendBufferSize directive then the respective value is inherited from the main server. (That is, inherited from whatever the final setting of that value is in the main server.)
- The "lookup defaults" that define the default directory permissions for a vhost are merged with those of the main server. This includes any per-directory configuration information for any module.
- The per-server configs for each module from the main server are merged into the vhost server.
- Essentially, the main server is treated as "defaults" or a "base" on which to build each vhost. But the positioning of these main server definitions in the config file is largely irrelevant -- the entire config of the main server has been parsed when this final merging occurs. So even if a main server definition appears after a vhost definition it might affect the vhost definition.
- Any vhost that includes the magic _default_ wildcard is given the same ServerName as the main server.

## Virtual host matching

The server determines which vhost to use for a request as follows:

#### IP address lookup

When the connection is first received on some address and port, the server looks for all the VirtualHost definitions that have the same IP address and port.

If there are no exact matches for the address and port, then wildcard (*) matches are considered.

If no matches are found, the request is served by the main server.

If there are VirtualHost definitions for the IP address, the next step is to decide if we have to deal with an IP-based or a name-based vhost.

#### IP-based vhost

If there is exactly one VirtualHost directive listing the IP address and port combination that was determined to be the best match, no further actions are performed and the request is served from the matching vhost.

#### Name-based vhost

If there are multiple VirtualHost directives listing the IP address and port combination that was determined to be the best match, the "list" in the remaining steps refers to the list of vhosts that matched, in the order they were in the configuration file.

If the connection is using SSL, the server supports Server Name Indication, and the SSL client handshake includes the TLS extension with the requested hostname, then that hostname is used below just like the Host: header would be used on a non-SSL connection. Otherwise, the first name-based vhost whose address matched is used for SSL connections. This is significant because the vhost determines which certificate the server will use for the connection.

If the request contains a Host: header field, the list is searched for the first vhost with a matching ServerName or ServerAlias, and the request is served from that vhost. A Host: header field can contain a port number, but Apache always ignores it and matches against the real port to which the client sent the request.

The first vhost in the config file with the specified IP address has the highest priority and catches any request to an unknown server name, or a request without a Host: header field (such as a HTTP/1.0 request).


## Source:

- [Apache documentation][apache_virtual_host]



[apache_virtual_host](https://httpd.apache.org/docs/2.4/vhosts/)
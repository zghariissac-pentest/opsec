# DNS Leak Tester

## Purpose

DNS requests reveal how domain names are translated into IP addresses.

Even when a user changes network routing, DNS behavior may still expose information about the network configuration.

---

## Why DNS Matters

DNS traffic can reveal:

1 Browsing destinations

2 Resolver ownership

3 Geographic information

4 Infrastructure choices

---

## Common Exposure Sources

1 Default ISP resolvers

2 Misconfigured VPN environments

3 Operating system fallback behavior

4 Split tunnel configurations

---

## Operational Review

Questions to ask:

Who operates the resolver?

Does the resolver match the expected environment?

Are multiple resolvers configured?

Are response patterns consistent?

---

## Key Principle

Network routing and name resolution should be evaluated together.

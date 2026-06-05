# Firewall Rules

## Purpose

A firewall controls which network traffic is allowed to enter or leave a system.

---

## Security Goals

Reduce attack surface

Control exposure

Monitor unexpected services

Restrict unnecessary access

---

## Inbound Traffic

Inbound traffic originates from external systems.

Only required services should be reachable.

---

## Outbound Traffic

Outbound traffic originates from the local system.

Unexpected outbound traffic can indicate:

Application misconfiguration

Unauthorized software

Data exposure risks

---

## Common Principles

Default deny when possible

Allow only required services

Review rules regularly

Remove unused exceptions

Document changes

---

## Operational Review

Questions to ask:

Which ports are exposed?

Why are they exposed?

Who needs access?

What happens if access is removed?

---

## Key Principle

Every open service increases exposure.

Exposure should always have a reason.

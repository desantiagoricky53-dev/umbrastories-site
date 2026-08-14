# Spacemail aliases — manual setup steps

> **These are manual account-settings steps for Rico to do in the Spaceship
> dashboard.** Nothing here is automated and nothing in the repo depends on it.

## Why aliases (and not new mailboxes)

The five real mailboxes on umbrastories.studio — `dev@`, `me@`, `latam@`,
`us@`, `workflow@` — are **reserved as TikTok account logins**. Don't use them
for public correspondence, and don't burn new mailboxes on it either. Aliases
give out clean public addresses (`submit@`, `hello@`, `press@`) while the mail
lands in one mailbox you actually read.

## Steps (Spaceship dashboard)

1. Log in at spaceship.com and open the **Spacemail** panel for
   `umbrastories.studio`.
2. Pick the mailbox that should receive human correspondence — whichever of
   the five you prefer to read (e.g. `me@`). All three aliases below route
   into that one mailbox.
3. Find the alias section — depending on dashboard version it's labeled
   **Aliases**, **Email aliases**, or lives under the mailbox's settings.
4. Add these three aliases, each pointing at the mailbox from step 2:
   - `submit@umbrastories.studio` — story submissions correspondence
     (pairs with the `/submit` form link used in videos)
   - `hello@umbrastories.studio` — general contact
   - `press@umbrastories.studio` — media / collab inquiries
5. Save, then test each alias: send one message to `submit@`, `hello@`, and
   `press@` from an outside account and confirm all three arrive in the
   chosen mailbox.

## Notes

- Aliases receive mail; replies are sent from the underlying mailbox. If you
  want replies to *appear* from an alias (e.g. answer as
  `hello@umbrastories.studio`), look for a "send as" / identity option in
  Spacemail's settings for that mailbox and add the alias there too.
- Do **not** create forwarding rules that auto-forward off-domain, and do not
  touch MX/SPF/DKIM/TXT records while in the DNS panel — mail is live.

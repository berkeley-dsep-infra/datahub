# Communicating with our end users

Currently, we do not have a mechanism to communicate our *expectations* of
end users to our end users. This is done in an ad-hoc way through talks with
instructors, and a post-hoc way when users log in to their hubs *after* their
files have been archived. Users do not have clear guidance on how to be good
citizens of the hub. It is important we provide this at crucial junctures,
rather than have them find that they have run afoul of some policy unintentionally
*after* the fact.

## Welcome email

A very common theme now when you sign up for a service is a [welcome
email](https://blog.hubspot.com/marketing/welcome-email-examples) that lands
in your inbox on first sign-in. This usually has a friendly greeting, information
on where to find help, and perhaps an unsubscribe link.

Many of our users don't even know they're using a 'JupyterHub' - this is intentionally
done, so they can click an nbgitpuller link and immediately get to their content
in a notebook or RStudio. This provides no clear pathway to give them information
about what a JupyterHub is, or what policies related to storage or usage are. A
welcome email sent when a user *first logs in* to a JupyterHub can help here, as
it helps us provide information without blocking their educational workflow.

This email should contain:

1. A friendly greeting, in an appropriate tone
2. Information on storage & usage policies
3. A link to our docs, where they can learn more (if appropriate)

As this is done on a *per hub* basis, this also allows us to set different policies
for different hubs. For example, a class specific hub might get the home directories
of people who do not log in wiped out after a 6 month period - this is alright as long
as we *inform users well beforehand*. The welcome email will help us do this.

## Storage enforcement notification emails

Users' home directories are the most precious asset we have in our infrastructure,
and something that should be protected at all costs. Data loss can be devastating
to someone's coursework or later on, their career. It's important that users know
*how* their home directories are handled with clarity. We will provide some of this
in the welcome email, but storage policies imply enforcement actions - and we will
need to send out notification emails for these too. At least the following actions
should trigger notifications:

1. When a user's home directory matches the threshold for archival. This should
   contain instructions on how they can either download their home directory,
   or do some action that marks their account as 'active'.
2. When a user's home directory is archived. This should contain instructions on
   how they can retrieve their home directory.
3. When a user's archived home directory is about to be deleted. We should send
   at least two notices a week apart. It should contain instructions on how
   to retrieve their files.

## One time email to current users

We already have thousands of users, and no welcome email was sent for them.
We might need to do a one-shot specially crafted email to everyone, active now
and in the past.
.. _finances:

========
Finances
========

Resource consumption and spending can be tracked and managed at our cloud
providers and we log this usage in a Google doc.

Google Cloud
============

Deployment assets are organized into projects and those projects have linked billing accounts. A project can be linked to only one billing account, however a billing account can be linked to more than one project. The accounts may be backed by grants or credit cards and can be switched out when needed. The current billing account runs through 1/2020.

We configure the billing accounts to export billing JSON to cloud buckets. These may be consumed by tools such as notebooks for later analysis.

Azure
=====

Azure resources are affiliated with "subscriptions" that are backed by "sponsorship". The latter are managed at `a sponsorship portal <https://www.microsoftazuresponsorships.com>`_.

Datahub Spend Waterfall
=======================

We track week-to-week spending in a Google Sheet owned by ds-instr@berkeley.edu. Each sheet in the document represents the finances for one of our cloud providers for a given term. Each week's spend is from Wed. through Tue. and we log the previous week every Wed.

In the Google billing console, go to Reports. Make sure to enable "Discounts" beneath the Credits heading, but disable "Promotions". The latter represents our grants. Set a custom date range for the prior week.

In the Azure sponsorship portal, login as the ds-instr@berkeley.edu account and visit Usage. Here too one must also set a custom date range for the prior week.

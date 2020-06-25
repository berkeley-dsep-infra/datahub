# 2018-06-11 - Azure billing issue causes downtime

## Summary

On June 11, 2018, the cloud vendor notified ds-instr that the data8-17f-prod subscription was canceled due to its usage cap. The educator portal confirmed that the spend had surpassed the budget. After additional funds were allocated to the subscription, a portion of the VMs were manually started. The hub came back online after pods were forcibly deleted and nodes were cordoned.

## Timeline

### 2018-06-11 9:02a

ds-instr received an email from the cloud vendor:

> The following subscriptions under your Microsoft Azure sponsorships for ds-instr@berkeley.edu have recently become canceled.
> Because these subscription(s) are canceled, all services have been suspended but no data has been lost. You have 90 days from the date of cancellation before Microsoft will delete the subscription and all attached data. Please use the Educator Portal to reactivate the subscription(s).

| Subscription Name | Subscription Id | Canceled Reason       |
| ----------------- | --------------- | --------------------- |
| data8-17f-prod    | *omitted here*  | Subscription Cap      |

### 9:29

The subscription status was confirmed at https://www.microsoftazuresponsorships.com/Manage. In order to allocate additional budget to data8-17f-prod, budget for other subscriptions had to be reduced.

### 9:40

VMs were turned on at https://portal.azure.com: 3 nodes in each node pool, the nfs server, the kubernetes master, and the database server.

### 9:45

The hub was unreachable even though the VMs were online. The hub and proxy pods were shown as Running and all nodes were shown as online even though some nodes had not been started. The offline cluster nodes were manually cordoned. All pods had to be forcibly deleted before they would start.

### 10:14

The Billing Alert Service was checked at https://account.azure.com/Subscriptions/alert?subscriptionId=06f94ac5-b029-411f-8896-411f3c6778b4 and it was discovered that alerts were no longer registered.

## Conclusion

There were insufficient funds on the subscription to persist its resources. The subscription budget was increased and the hub was brought back online. The billing alert service that was configured to prevent such incidents did not function properly.

## Action items

### Process

1. Do not use subscription portal billing alerts.
1. Manually check subscription usage via an unattended process.

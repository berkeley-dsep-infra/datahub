# Summary

On October 10, 2017, the cloud vendor notified ds-instr that the data8r-17s subscription was canceled due to its end date, and we had 90 days to reactivate it using the educator portal. A support ticket was created to reverse the cancellation since the educator portal did not permit reactivation. On October 18 we were notified that the subscription's resources were deleted.

Coincidentally, a script was written on Oct. 9 to backup data to ds-instr's Google Drive and it was performed for the instructor as a test. Unfortunately it wasn't run for all users before the resources were taken offline.

## Timeline

### 2017-10-10 9:06a

ds-instr received an email from the cloud vendor:

> The following subscriptions under your [cloud vendor] sponsorships for ds-instr@berkeley.edu have recently become canceled.
> Because these subscription(s) are canceled, all services have been suspended but no data has been lost. You have 90 days from the date of cancellation before [the cloud vendor] will delete the subscription and all attached data. Please use the Educator Portal to reactivate the subscription(s).

| Subscription Name | Subscription Id | Canceled Reason       |
| ----------------------------------------------------------- |
| data8r-17s        | <snip>          | Subscription End Date |

### 9:30

The instructor was notified. The educator portal did not provide a way to view or alter the subscription end date of a canceled subscription so a support request was filed at the cloud vendor.

### 11:14

The cloud vendor asks that a payment instrument be added to the ds-instr account. We respond that the account is funded by a sponsorship.

### 17:22

The cloud vendor contacts their sponsorship team.

### 2017-10-11 15:00

The cloud vendor calls to discuss the situation. Screenshots of the educator and cloud portal were sent to the cloud vendor.

### 2017-10-12 16:19

The cloud vendor offers to enable the subscription for a 60 minute period from the backend so that the End Date may be extended from the portal. Though the subscription is re-enabled for an hour, the portal still does not permit the subscription parameters to be changed.

### 2017-10-18 15:29

The cloud vendor says that the subscription was actually disabled because it had exhausted the allocated funds, and the data was deleted within 24 hours despite the stated 90 day grace period. Later the following was provided by the cloud vendor:

> I worked with our backend engineering team last night and I am afraid to say that we could not retrieve the storage account after all our sincere efforts. I understand how frustrating it would be for you and I do not have the words to express the same, I just wish if I could be of some help to you.
>
> Having said that we did dig into the reasons behind this situation, the subscription was initially suspended by an internal engineering job occurred that auto-suspended all Academic Account Sponsorship subscriptions with an end date that was part of the previous fiscal year. Usually this suspension does not delete the subscription. There are a few [cloud vendor] accounts which are on legacy commerce platform which are affected and these accounts are in the process of modern platform. Your account was in the transition mode when the subscription got suspended and your account was partially converted to the modern platform. The billing & subscription part was converted to the modern platform but the not at the service level. Hence you got the message that your data would be retained for 90 days, at the same stated at the service level it was not converted to the modern hence the data got deleted.
>
> I had a detailed discussion with our product group team on this and how we can avoid this in future. First of all, your account is now completely migrated/transitioned completely to the modern platform. Also, to ensure that our other Academic Account Sponsorships customers do not face the same issue they have agreed to complete the migration manually on those accounts.

### 2017-10-19 10:53

The cloud vendor compensates ds-instr with an additional $10k for the experience.

## Conclusion

There were insufficient funds on the subscription to persist its resources. The resources were deleted by the cloud vendor before the grace period ran out.

## Action items

### Process

1. Until there is a per-user backup implemented hub-side, set a schedule for backing up user data for every course.
1. Always set a billing alert at some conservative amount less than the subscription alotment
1. If a subscription is ever canceled, backup user data within 24 hours, regardless of the stated grace period.

# Storage Policy

The goal of this policy document is to develop a short-term and long-term policy outlook for storing user data across all hubs.

Currently (as of 5/18/2021), our disk storage snapshot looks like this below. We have 23 TB of storage accumulated across all disks. 

![alt text](storage_snapshot.PNG "Snapshot of storage across all disks")

## Policy proposal for users with home directory size greater than 100 GB

Policy proposal seeks to address the question "How do we handle scenarios where **users stored more than the archival threshold (~100 GB of data)** in their home directories?"

Currently, we don't have a clearly defined policy for storage that can be communicated to our end users. In addition, we don't have system level feedback loops for users to know whether they are violating certain storage policy restrictions.

Due to above challenges, We found [multiple instances](https://docs.google.com/document/d/1KsMmRq4rf40kEazQYwEgFpaz__N7-yauG9nvN-3C3lw/edit?usp=sharing) where users stored more than 100 GB worth of data during the recent disk storage analysis. Such users home directory size approximates to around ~3 TB of storage which includes large and complex datasets. Interestingly, Many users did not even log into their instances of the hub during the past 6 - 12 months. Note that, **users had no way of knowing whether they stored large files in the home directories**. Sharing couple of examples which could have been avoided if we had proactively communicated our storage policy and provided system level feedback for users,

One of the user home directory snapshotted below had a database file named "fec_nyc.db" whose size was around ~900 GB of data. This database file was used as part of the Data 100 course lab 4 where students learn to work with a database using the SQLAlchemy package. 

![alt text](user2_snapshot.png "Single database file whose size is 900 GB")

Another user had a core.rsession file whose size was around 785 GB. She had this file under the course directory PH142_Fall2019 (Ph142 is the abbreviation for the course "Introduction to Probability and Statistics in Biology and Public Health").

![alt text](user1_snapshot.png "Single Rsession file whose size is 785 GB")

Accumulated file sizes of all such home directories would run into to few TB. Inorder to avoid such scenarios, we need to proactively communicate our policies to users and on a monthly basis run jobs to measure and visualize disk size. It will help us to identify and provide useful feedback to users (**who do not have any systematic way of knowing whether their home directory size violates a storage policy**) about their storage.

The policy recommendation is to **Run an archival job every week and archive any user's home directories with a size greater than 100 GB which is not yet been accessed for the past 90 days**. Infra team should reach out to the concerned user(s) to inform them about their current storage status.

In addition, Infra team should communicate our storage policies proactively to all users (including instructors/GSIs) through a welcome message when they log in to Datahub.

## Policy proposal for users home directory archival

Policy proposal seeks to address the question "How can we redesign our storage archival policy so that it is user centric for *all users* while  simplifying the effort and cost involved at the infra admin end"

As shown in the snapshot below, We had 54 archival requests in total during the course of past two semesters (from Sep, 21 to May, 22). 

![alt text](archival_request.PNG "Archival requests during Fall 2021 and Spring 2022")

Less than 1% (~50) of all Datahub users (~10k) make data archival requests. Almost all of these requests are from users who are from couple of Data classes. 99% of the archival requests were made for two different hubs - Datahub and Data 100 hubs. 

We can hypothesize that most users using other hubs are either a) not aware that they can request their data post the completion of their courses or b) do not need to retrieve their data. Assuming option a, If we plan to improve our outreach message to ensure that all users are aware of the archival process, we may still run into issues with our capacity to handle such requests. We collectively identify that the manual storage archival process is something we want to move away from via automation.

As part of this policy proposal, let's explore multiple policy options to handle this scenario.

### Policy options to be considered:

**Option #1:**
Keep the archival service as-is while automating the entire process in the near term. 

In addition, Increase the outreach to all instructors to ensure that all users have equitable access to their data once their course gets completed. Communicate our storage policies to all users through a welcome message when they log in to Datahub.

**Pros:** 
- More users beyond Data 100 and Datahub will have awareness about retrieving their data

**Cons:**
- Storage keeps increasing with additional cloud costs incurred for the infra team
- Additional effort for the infra team to manage storage-related tasks like responding to archival requests, reviewing storage consistently, increasing storage when disk size is nearly full, etc.

**Option #2:** 
Eliminate archival process completely. Allow users to download all their Hub data up to 3 months from the time of their course completion. Data gets deleted from the hub after the completion of 3 months.

Send automated alerts at consistent intervals during this period to ensure that users are aware of the impending deadline.

**Pros:** 
- Eliminate archival requests completely by proactively asking users to back up their files.
- Significant cloud cost savings at our end
- Hub admin's time saved from responding to all archival requests
- Need not invest infrastructure efforts to automate archival requests

**Cons:**
- 10 - 15% of users who reach out for archival requests may fail to back up their files despite the repeated nudges

**Option #3:**
Archive only the notebook files (files with ipynb,rmd, .r, and .jl extensions) having code. The rest of the non-notebook files including the datasets are deleted after 3 months of course completion. Or the datasets could be stored in a shared read directory or google drive from where students can import them into their notebooks. 

**Pros:**
- Users can request their notebook files months after their course completion.
- Significant cloud cost savings at our end as most notebook files are smaller in file size in comparison to the datasets
- Can automate only this part of the archival process if required

**Cons:**
- The workload for hub admins to respond to archival requests remains the same
- Deciding which files to archive can be a complex activity for the admin
- Users will not have access to their datasets

**Policy Decision:**
We prefer option #1 where we want to automate the entire archival process in the longer run. However, in the near term, we plan to take effective measures to a) make our storage related process and policy user centric (Ref #3388) and b) optimize our cloud costs through exploring different tiers of storage (Ref #3389).
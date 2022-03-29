#Policy considerations while creating a new hub

We have mastered creating new hubs based on our prior experience creating 10+ hubs catering to the diverse needs of the instructors across the campus. Our decisions with regards to creating a new hub were made with a lot of intuition around solving instructors' needs effectively within the time constraints.
The objective of this policy document is to verbalize our heuristics for creating a new hub so that it can guide the decision making of all team members in the future. 

- Course has a large user base with more than 300+ students (Eg: Data 8 and Data 100 hubs)
- Course is computationally intensive and requires a large amount of CPU/Memory requirements (RAM greater than 2 GB or requires the use of calendar-based scheduling on a weekly basis) like a biology hub
- Testbed for deploying new features which post maturity can be enabled across other major hubs (Eg: Stat 159 hub)
- Course requirements tend to be dynamic and require making more than 5+ CI/CD deployments every month (Eg: Stat 159 hub)
- Course has a specific requirement for specific packages which are incompatible with the standard package version listed in Datahub (Eg: Astro hub)
- Course has undergrad students acting as GSIs while requiring admin access (Eg: Data8 hub)
- Hub is created for organizational/strategic reasons to build institutional buy-in from specific departments (Eg: Public Health and ISchool Hubs)
- Hub is created for organizational/strategic reasons to evangelize a specific service (Eg: Julia or R hub)
- Policy changes for deployment to the main Datahub
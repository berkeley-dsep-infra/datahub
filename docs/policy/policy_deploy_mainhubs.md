
# Policy considerations for deploying to the main Datahub

Our goal is to provide a reliable infrastructure that instructors can completely trust while facilitating their coursework. Developing a robust protocol around deploying changes to the main datahub is important to achieve this goal. The objective of this policy document is to outline the criteria to deploy a change to an image in the main Datahub.

- Regular requests during the semester like package addition/change, RAM increase, CPU allocation, and providing admin access to users should be done with a robust testing protocol (either automated or manual) in place across staging and production.
- Introduce new features in the main Datahub only after it gets successfully tested with one or many instructors across other course specific hub (eg: Data8 Hub) or use-case specific hub (Eg: Stat159 Hub).
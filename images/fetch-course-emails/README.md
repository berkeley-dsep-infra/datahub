fetch-course-emails
-------------------

This container fetches the campus email addresses of students and instructors
in specified UCB courses. It runs as a sidecar container alongside hubs
provisioned by berkeley-dsep-infra/datahub.

Configuration
=============

Container
=========

This container is run as a sidecar by specifying it under hub.extraContainers.
Provide API credentials as environment variables in encrypted configuration (i.e. secrets):
```
jupyterhub:
  hub:
    extraContainers:
      - name: fetch-course-emails
        image: berkeleydsep/fetch-course-emails:v3
        volumeMounts:
          # for writing out email lists ; consider new volume
          - name: hub-db-dir
            mountPath: /srv/jupyterhub
          # for reading in profiles
          - name: config
            mountPath: /etc/jupyterhub/config
        env:
        - name: UCB_HR_ID
          value: "..."
        - name: UCB_HR_KEY
          value: "..."
        - name: SIS_CLASSES_ID
          value: "..."
        - name: SIS_CLASSES_KEY
          value: "..."
        - name: SIS_ENROLLMENTS_ID
          value: "..."
        - name: SIS_ENROLLMENTS_KEY
          value: "..."
        - name: SIS_STUDENTS_ID
          value: "..."
        - name: SIS_STUDENTS_KEY
          value: "..."
        - name: SIS_TERMS_ID
          value: "..."
        - name: SIS_TERMS_KEY
          value: "..."
```

Profiles
========
Courses are specified as keys of the form {year}-{term}-{class_section_id} in
the helm config. For example:

```
custom:
  profiles:
    2019-summer-15798: {}
    2019-spring-25622:
      mem_limit: 4096M
      mem_guarantee: 2048M
```

See https://classes.berkeley.edu for class section IDs.

Output
======
The container saves email addresses into files:
```
/srv/jupyterhub/profiles.d/{year}-{term}-{class_section_id}-students.txt
/srv/jupyterhub/profiles.d/{year}-{term}-{class_section_id}-instructors.txt
```
which are read by the custom spawner.

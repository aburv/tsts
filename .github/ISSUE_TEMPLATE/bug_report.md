name: Bug report
description: Create a bug report to help us improve the project
title: "[Bug]: "
labels: [Bug]
assignees:
- guru-aburv
body:
- type: markdown
  attributes:
    value: |
      Thanks for taking the time to fill out this bug report.
- type: checkboxes
  attributes:
    label: Is there an existing issue for this?
    options:
    - label: I have searched the existing issues
      required: true
- type: textarea
  attributes:
    label: Description
    description: A concise description of what you're experiencing and what you expect.
    placeholder: |
      When I do <X>, <Y> happens and I see the error message attached below:
      ```...```
      What I expect is <Z>
  validations:
    required: true
- type: dropdown
  id: platform
  attributes:
    label: Platform
    description: "Platform where the issue is reproducible"
    options:
        - Android
        - Web
        - Ios
  validations:
    required: true
- type: input
  id: version
  attributes:
    label: Version
    description: "The version of the app"
    placeholder: "App version is present inside App -> about"
  validations:
    required: true
- type: textarea
  attributes:
    label: Steps To Reproduce
    description: Add steps to reproduce this behaviour, include console / network logs & videos
    placeholder: |
      1. Go to '...'
      2. Click on '....'
      3. Scroll down to '....'
      4. See error
  validations:
    required: true
- type: dropdown
  id: severity
  attributes:
    label: Severity
    description: "The impact of the issue"
    options:
        - Low (Cosmetic UI issues)
        - Medium (Frustrating UX)
        - High (Blocker to building or releasing)
        - Critical (Broken Production apps)
  validations:
    required: true
- type: input
  id: video
  attributes:
    label: Issue video log
    description: "Share a loom video recording of how the issue can be reporduced"
    placeholder: "https://www.loom.com/share/d54e04bc68e24798..."
  validations:
    required: false

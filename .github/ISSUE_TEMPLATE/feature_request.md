name: Feature request
description: Suggest an idea to improve appsmith
title: "[Feature]: "
labels: [Enhancement]
assignees:
- guru-aburv
body:
- type: markdown
  attributes:
    value: |
      Thanks for taking the time to request a feature!
- type: checkboxes
  attributes:
    label: Is there an existing issue for this?
    description: Please search to see if an issue related to this feature request already exists.
    options:
    - label: I have searched the existing issues
      required: true
- type: textarea
  attributes:
    label: Feature in detail
    description: Describe the feature in detail.
  validations:
    required: true
- type: textarea
  attributes:
    label: Impact via this feature.
    description:  Tell us how the users are benefited with this
  validations:
    required: true

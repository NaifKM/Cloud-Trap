# The console can't turn this on. Run it in CloudShell after creating the rule.
aws events put-rule \
  --name cloud-trap-rule \
  --event-pattern file://event-pattern.json \
  --state ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS

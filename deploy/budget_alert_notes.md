# Budget alert and deployment evidence

- **Threshold:** $5 monthly budget; email warning at 80% actual spend ($4), plus forecast warning at 100%.
- **FinOps tags/labels:** service=`afyaplus-triage`, environment=`capstone`, owner=`week7-student`, cost-center=`ai-platform`.
- **Evidence to capture:** actual budget name/scope, amount/currency, threshold, recipient, created timestamp, and a screenshot of the console/API response.
- **AWS:** `aws_budget.json` is shaped as the `Budget` plus `NotificationsWithSubscribers` used by the AWS Budgets create-budget request. Replace the email and submit using an authorized account ID and regionless Budgets API/CLI workflow.
- **Azure:** `azure_budget_triage.json` is an illustrative properties body. Use the current Cost Management Budgets REST API for the exact scope and API version; do not treat the file as proof of creation.
- **Important:** alerts are not hard caps and billing data may be delayed. Set provider-side quotas/rate limits where available, cap output tokens, restrict keys, and monitor actual usage. Do not commit secrets.

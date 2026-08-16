## Databricks Workspace Migration & Quota Issue

- After Key Vault integration, attempted to restart/recreate cluster in original workspace (Hospital-ADB) - failed with "exhausted available credits" error despite sufficient Azure balance
- Root cause: original workspace was created under "Trial (Premium - 14-Days Free DBUs)" - this trial-specific compute allocation expired independently of overall Azure subscription credit
- Attempted fix 1: Upgraded Azure subscription from Free Trial to Pay-As-You-Go (Cost Management + Billing > Subscriptions > Upgrade) - confirmed successful, but cluster creation still failed with same error (likely stale trial-state flag stuck on the old workspace object)
- Attempted fix 2: Tried Serverless compute as a workaround - notebook ran successfully, but hit a new blocker: spark.conf.set() for ADLS storage key is NOT supported on Serverless compute (CONFIG_NOT_AVAILABLE error) - this method only works on all-purpose clusters
- Decision: Created a brand new Databricks workspace (Hospital-ADB-v2, Hybrid type, Premium tier, Central India) under the now-upgraded subscription, avoiding the trial allocation entirely
- New blocker: AZURE_QUOTA_EXCEEDED_EXCEPTION when creating all-purpose cluster - subscription had 0 vCPU quota for Standard DDSv5 Family in Central India (common for new/upgraded subscriptions)
- Fix: Submitted a quota increase request (Azure Portal > Quotas > My Quotas > Standard DDSv5 Family vCPUs > Central India > New Quota Request, requested limit: 8) - request currently under review

## Key Learnings
- Databricks trial DBU allocations are separate from general Azure subscription credit - both can independently run out
- Serverless compute has real limitations (can't set raw Hadoop/Spark storage configs) - not a drop-in replacement for all-purpose clusters for all use cases
- New/upgraded Azure subscriptions often start with 0 default vCPU quota per region/VM family - requires explicit quota increase request before first cluster creation
- Azure Databricks billing/quota issues sometimes require creating a fresh workspace rather than fixing an existing one, especially after subscription-tier changes
## Steps After Migration
- Re-linked Key Vault secret scope to new workspace (same scope name: hospitalanalyticsvaultscope) - no notebook code changes needed
- Copied bronze notebook (Key Vault-based version) into new workspace, attached to new cluster
- Ran local simulator + bronze notebook together to test end-to-end
- Verified success via display(df) - real patient records visible, including intentional dirty data (age: 134)
- Bronze layer fully functional on new workspace
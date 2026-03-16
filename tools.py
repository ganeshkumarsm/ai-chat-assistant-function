from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import os

SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

credential = DefaultAzureCredential()

compute_client = ComputeManagementClient(
    credential,
    SUBSCRIPTION_ID
)


def restart_virtual_machine(resource_group, vm_name):

    poller = compute_client.virtual_machines.begin_restart(
        resource_group,
        vm_name
    )

    poller.result()

    return f"Virtual machine {vm_name} restarted successfully."
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

    print(f"Restarting VM {vm_name} in {resource_group}")

    compute_client.virtual_machines.begin_restart(
        resource_group,
        vm_name
    )

    return f"Restart initiated for VM {vm_name}"
<<<<<<< HEAD

def stop_virtual_machine(resource_group, vm_name):

    compute_client.virtual_machines.begin_deallocate(
        resource_group,
        vm_name
    )

    return f"Shutdown initiated for virtual machine {vm_name}"
=======
>>>>>>> 39a73491f5e7b181e1717ba963bd02a205fa73e1

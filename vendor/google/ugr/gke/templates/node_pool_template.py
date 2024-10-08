"""Creates a GKE node pool with specific configurations."""


def GenerateConfig(context):
    """Generates the YAML resource configuration for a node pool."""

    pool_name = context.properties["poolName"]
    cluster_name = context.properties["clusterName"]
    region = context.properties["region"]
    date_suffix = context.properties["dateSuffix"]  # Format: yyyy-mm-dd
    initial_node_count = context.properties["initialNodeCount"]
    disk_size_gb = context.properties["diskSizeGb"]
    machine_type = context.properties["machineType"]
    min_node_count = context.properties["minNodeCount"]
    max_node_count = context.properties["maxNodeCount"]

    resources = [
        {
            "name": f"user-{pool_name}-{date_suffix}",
            "type": "gcp-types/container-v1:projects.locations.clusters.nodePools",
            "properties": {
                "parent": f'projects/{context.env["project"]}/locations/{region}/clusters/{cluster_name}',
                "nodePool": {
                    "name": f"{pool_name}-pool",
                    "initialNodeCount": initial_node_count,
                    "config": {
                        "machineType": machine_type,
                        "diskSizeGb": disk_size_gb,
                        "diskType": "pd-balanced",
                        "imageType": "COS_CONTAINERD",
                        "labels": {"hub.jupyter.org/pool-name": f"{pool_name}-pool"},
                        "taints": [
                            {
                                "key": "hub.jupyter.org_dedicated",
                                "value": "user",
                                "effect": "NO_SCHEDULE",
                            }
                        ],
                        "tags": ["hub-cluster"],
                    },
                    "autoscaling": {
                        "enabled": True,
                        "maxNodeCount": max_node_count,
                        "minNodeCount": min_node_count,
                    },
                    "management": {"autoUpgrade": False, "autoRepair": True},
                },
            },
        }
    ]

    return {"resources": resources}

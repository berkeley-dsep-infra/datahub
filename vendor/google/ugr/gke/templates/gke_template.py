"""Creates a GKE cluster with specific configurations."""


def GenerateConfig(context):
    """Generates the YAML resource configuration."""

    project = context.env['project']
    cluster_name = context.properties['clusterName']
    region = context.properties['region']
    pool_name = context.properties['poolName']
    date_suffix = context.properties['dateSuffix']  # Format: yyyy-mm-dd
    node_location = context.properties['nodeLocation']
    initial_node_count = context.properties['initialNodeCount']
    disk_size_gb = context.properties['diskSizeGb']
    machine_type = context.properties['machineType']
    min_node_count = context.properties['minNodeCount']
    max_node_count = context.properties['maxNodeCount']

    resources = [{
        'name': cluster_name,
        'type': 'gcp-types/container-v1:projects.locations.clusters',
        'properties': {
            'parent': f'projects/{project}/locations/{region}',
            'cluster': {
                'name': cluster_name,
                'initialClusterVersion': 'latest',
                'location': region,
                'locations': [node_location],
                'ipAllocationPolicy': {
                    'useIpAliases': True
                },
                'addonsConfig': {
                    'httpLoadBalancing': {
                        'disabled': True
                    }
                },
                'nodePools': [{
                    'name': f'{pool_name}-{date_suffix}',
                    'initialNodeCount': initial_node_count,
                    'config': {
                        'diskSizeGb': disk_size_gb,
                        'diskType': 'pd-balanced',
                        'machineType': machine_type,
                        'imageType': 'COS_CONTAINERD',
                        'labels': {
                            'hub.jupyter.org/pool-name': f'{pool_name}-pool-{date_suffix}'
                        },
                        'oauthScopes': [
                            'https://www.googleapis.com/auth/compute',
                            'https://www.googleapis.com/auth/devstorage.read_only',
                            'https://www.googleapis.com/auth/logging.write',
                            'https://www.googleapis.com/auth/monitoring',
                            'https://www.googleapis.com/auth/servicecontrol',
                            'https://www.googleapis.com/auth/service.management.readonly',
                            'https://www.googleapis.com/auth/trace.append'
                        ],
                    },
                    'autoscaling': {
                        'enabled': True,
                        'maxNodeCount': max_node_count,
                        'minNodeCount': min_node_count
                    },
                    'management': {
                        'autoUpgrade': False,
                        'autoRepair': True
                    },
                    'locations': [
                        node_location
                    ]
                }],
                'networkPolicy': {
                    'enabled': True
                }
            }
        }
    }]

    return {'resources': resources}

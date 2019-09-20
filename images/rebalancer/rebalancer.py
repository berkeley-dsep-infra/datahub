#!/usr/bin/env python3
"""
Rebalance placeholder pods so they are always on the newest node

When a new node is brought up by the autoscaler, it doesn't have any of our
user images. So for about 10 mintues (which is how long our biggest image takes to pull!),
user pods that end up on that node time out (which is 5 minutes now). This is despite
the fact that older nodes with images present already have space that's taken up
by user placeholder pods.

So whenever a new node comes up, we label it and send the user placeholder pods there.
This isn't the most elegant, generalized or correct solution, but it works for now.

"""
import logging
import asyncio
import aiohttp
from kubernetes_asyncio import client, config
import backoff

# FIXME: Make these configurable
namespace = 'datahub-prod'
attractor_label = 'hub.jupyter.org/attract-placeholders'
user_node_selector = 'hub.jupyter.org/node-purpose=user'


# FIXME: More precise list of exceptions we want to retry on
@backoff.on_exception(backoff.expo, exception=aiohttp.ClientError)
async def label_newest_node(v1, namespace, user_node_selector, attractor_label):
    # sort nodes in ascending order of creation time
    nodes = sorted((await v1.list_node(label_selector=user_node_selector)).items, key=lambda n: n.metadata.creation_timestamp, reverse=True)

    # Scheduler won't schedule any of our placeholder pods if our labeled node isn't
    # marked as 'Ready', so we only operate on 'Ready' nodes
    # FIXME: Label unready nodes, but wait for them to be ready before killing placeholders
    ready_nodes = [
        node for node in nodes
        if any((c.type == 'Ready' and c.status == 'True' for c in node.status.conditions))
    ]

    # FIXME: Handle conflicts during patching operation
    labeling_event = False
    for i, node in enumerate(ready_nodes):
        if i == 0:
            # First node, ensure it has our attractor label
            if attractor_label not in node.metadata.labels:
                # Our youngest node doesn't have this label!
                node.metadata.labels[attractor_label] = 'true'
                await v1.patch_node(node.metadata.name, node)
                logging.info(f'Adding label to {node.metadata.name}')
                labeling_event = True
        else:
            if attractor_label in node.metadata.labels:
                # Setting value to None removes the labels
                node.metadata.labels[attractor_label] = None
                await v1.patch_node(node.metadata.name, node)
                logging.info(f'Removing label from {node.metadata.name}')
                labeling_event = True

    if labeling_event:
        logging.info('Deleting placeholder pods to move them to newest node')
        await asyncio.sleep(2)
        await v1.delete_collection_namespaced_pod(namespace, label_selector='component=user-placeholder')
    else:
        logging.info(f'Newest node {ready_nodes[0].metadata.name} already has appropriate label, no action performed')


async def main():
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    try:
        config.load_incluster_config()
        logging.debug('Acquired credentials from service account')
    except:
        await config.load_kube_config()
        logging.debug('Acquired credentials from kubeconfig')

    v1 = client.CoreV1Api()
    while True:
        await label_newest_node(v1, namespace, user_node_selector, attractor_label)
        await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
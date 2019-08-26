#!/usr/bin/env python

import yaml

configFiles = {}
DESTINATION = "productpage"

# start script
with open("sources/mem_quota.yaml", "r") as stream:
    try:
        docs = yaml.load_all(stream)
        for doc in docs:
            configFiles.update({doc['kind']: doc})
    except yaml.YAMLError as exc:
        print(exc)

# find the quota config
quotaHandler = configFiles.get('handler') if configFiles.get('handler')['spec']['compiledAdapter'] == 'memquota' else None

if not DESTINATION:
    print("Destination must not be empty")

quotas = quotaHandler['spec']['params']['quotas'][0]

# initial memory quota
requestRate = quotas['maxAmount']
rateInterval = quotas['validDuration']

# overide initial memory quota with relevant override quota configurations
overrides = quotas['overrides']
for quota in overrides:
    if 'dimensions' in quota and 'destination' in quota['dimensions']:
        if DESTINATION == quota['dimensions']['destination']:
            requestRate = quota['maxAmount']
            rateInterval = quota['validDuration']

# wie mach ich das wenn ich z.b. in der config 500/1s hab und aber will dass es 1500/3s sind?





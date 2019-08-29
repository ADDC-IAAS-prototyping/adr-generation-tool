#!/usr/bin/env python

import yaml

class Parser(object):
    def __init__(self, config_interval, config_rate, config_destination):
        self.config_interval = config_interval
        self.config_rate = config_rate
        self.config_destination = config_destination

    def collect_configurations_in_file(self, config_file):
        """Istio config files for rate limiting typically contain multiple configurations in one yaml file
        so we iterate through these configs and store them with their 'kind' property as key.
        """
        config_templates = {}
        for config in config_file:
            config_templates.update({config['kind']: config})
        return config_templates

    def get_quota_handler_configuration(self, config_templates):
        """Return Istio config with kind 'handler' if it is an memquota adapter"""
        return config_templates.get('handler') if config_templates.get('handler')['spec']['compiledAdapter'] == 'memquota' else ""
    
    def check_config(self, config_file):
        """Parse rate limit metrics from Istio configuration template file and check if the configuration is compliant
        with the user-defined configuration checks (config_rate, config_interval, config_destination).
        """
        if not self.config_destination:
            return 'Destination must not be empty for Istio rate limit configurations'
        else:
            config_templates = self.collect_configurations_in_file(config_file)
            config_quota_handler = self.get_quota_handler_configuration(config_templates)
            
            # if handler config template is of type memquota, get quotas, otherwise return error message
            if config_quota_handler:
                quotas = config_quota_handler['spec']['params']['quotas'][0]
            else:
                return 'No memquota handler found in this template file'

            # default memquota configuration
            template_rate = quotas['maxAmount']
            template_interval = quotas['validDuration']

            # refinements of default memquota configuration via overrides with stricter requirements
            overrides = quotas['overrides']
            for quota_override in overrides:
                if self.config_destination == quota_override['dimensions']['destination']:
                    template_rate = quota_override['maxAmount']
                    template_interval = quota_override['validDuration']
            
            return str('template_rate: {}, template_interval: {}\nconfig_rate: {}, config_interval: {}s'.format(template_rate, template_interval, self.config_rate, self.config_interval))
            
            
if __name__ == '__main__':
    parser = Parser(75, 90, "productpage")
    with open("sources/mem_quota.yaml", "r") as stream:
        try:
            docs = yaml.load_all(stream)
            print(parser.check_config(docs))
        except yaml.YAMLError as exc:
            print(exc)

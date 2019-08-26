import yaml
import rate_limit.kong.cli as kong

class RateLimitConfigChecker(object):
    def __init__(self, config_file):
        self.config_file = config_file
    
    def check_config_provider(self):
        """Check if keywords for providers are contained in the config - currently very naive checking for testing purposes.
        """
        if 'apiVersion' in self.config_file and 'config.istio.io/v1alpha2' in self.config_file['apiVersion']:
            return None # replace this with istio handler
        elif 'plugins' in self.config_file:
            kong.cli(self.config_file)
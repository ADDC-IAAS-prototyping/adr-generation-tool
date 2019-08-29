import click
import yaml
import rate_limit.kong.parser as kong
import rate_limit.istio.parser as istio

class RateLimitConfigChecker(object):
    def __init__(self, config_file):
        self.config_file = config_file


    def parsing_kong(self, config_file, config_interval, config_rate, config_destination):
        """Handler for kong rate limit config parser"""
        parser = kong.Parser(config_interval, config_rate)
        parsing_msg = parser.check_config(config_file)
        print(parsing_msg)


    def parsing_istio(self, config_file, config_interval, config_rate, config_destination):
        """Handler for istio rate limit config parser"""
        parser = istio.Parser(config_interval, config_rate, config_destination)
        parsing_msg = parser.check_config(config_file)
        print(parsing_msg)


    def cli(self, config_file, provider):
        """Start command line argument request and pass the resulting values to the parser initialization"""
        @click.command()
        @click.option('--interval', default=1, prompt='Enter interval for rate limit in s(econds) (mandatory)', help='Interval in s.')
        @click.option('--requestrate', default=1, prompt='Enter number of requests for this interval (mandatory)', help='Number of requests.')
        @click.option('--destination', default='', prompt='Enter ID of service or endpoint of destination (optional)', help='The person to greet.')
        def cli_params(interval, requestrate, destination):
            """CLI for basic configuration parameters for rate limit plugins"""
            if provider == 'kong':
                self.parsing_kong(config_file, interval, requestrate, destination)
            elif provider == 'istio':
                self.parsing_istio(config_file, interval, requestrate, destination)

        cli_params()


    def check_config_provider(self, path):
        """Check if keywords for providers are contained in the config - currently very naive checking for testing purposes."""
        for document in self.config_file:
            if 'apiVersion' in document and 'config.istio.io/v1alpha2' in document['apiVersion']:
                # new stream to clean load the file since self.config_file is a generator and pops elements while iteration
                with open(path, "r") as stream:
                    try:
                        self.cli(yaml.load_all(stream), 'istio')
                        break
                    except yaml.YAMLError as exc:
                        print("exc")
                        break
            elif 'plugins' in document:
                # typically kong rate limit templates consist of one configuration file so we just take this one
                self.cli(document['plugins'], 'kong')
                break
            else:
                continue
            
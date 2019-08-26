import click
import kong.parser as parsing

def cli(config_file):
    """Start command line argument request and pass the resulting values to the parser initialization.
    Since provider is KONG, the configuration file will be passed with the content of the 'plugins' property.
    """
    config_file = config_file['plugins']

    @click.command()
    @click.option('--interval', default=1, prompt='Enter interval for rate limit in s(econds) (mandatory)', help='Interval in s.')
    @click.option('--requestrate', default=1, prompt='Enter number of requests for this interval (mandatory)', help='Number of requests.')
    @click.option('--destination', default='', prompt='Enter ID of service or endpoint of destination (optional)', help='The person to greet.')
    def cli_config_params_kong(interval, requestrate, destination):
        """Simple CLI that asks for basic configuration parameters for kong rate limit plugins
        and returns the passed argument values.
        """
        parsing_handler(config_file, interval, requestrate, destination)

    cli_config_params_kong()


def parsing_handler(config_file, interval, requestrate, destination):
    """Call the actual parsing script with the entered config values from CLI.
    """
    parser = parsing.Parser(interval, requestrate)
    print(parser.check_config(config_file))
import click
import kong.parser as parser
import yaml

@click.command()
@click.option('--interval', default=1, prompt='Enter interval for rate limit in s(econds)', help='Interval in s.')
@click.option('--requestrate', default=1, prompt='Enter number of requests for this interval', help='Number of requests.')
@click.option('--destination', default='', prompt='Enter ID of service or endpoint of destination', help='The person to greet.')
def cli_config_params_kong(interval, requestrate, destination):
    """Simple CLI that asks for basic configuration parameters for kong rate limit plugins"""
    parsing = parser.Parser(interval, requestrate)
    with open("sources/rate_limit_example.yaml", "r") as stream:
        try:
            yamlfile = yaml.safe_load(stream)["plugins"]
            print(parsing.check_config(yamlfile))
        except yaml.YAMLError as exc:
            print(exc)
    # parser = kong.Parser(interval, requestrate, destination)

if __name__ == '__main__':
    cli_config_params_kong()
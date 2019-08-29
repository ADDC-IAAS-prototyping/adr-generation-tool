import click
import rate_limit.template_check as rate_limit
import yaml

PATH = "sources/config_template.yaml"

@click.command()
@click.option('--pattern-type', default='ratelimit', prompt='What pattern? (circuitbreaker/ratelimit)', type=click.Choice(['circuitbreaker', 'ratelimit']))
def pattern_checking(pattern_type):
    """Checks pattern type to be analyzed"""
    if pattern_type == 'ratelimit':
        config_check_rate_limit()


def config_check_rate_limit():
    """Open config file which have been stored in sources directory before executing the checker script.
    User must declare if it is a rate limit or circuitbreaker configuration template.
    """
    with open(PATH, "r") as stream:
        try:
            yamlfile = yaml.load_all(stream)
            config_checker = rate_limit.RateLimitConfigChecker(yamlfile)
            config_checker.check_config_provider(PATH)
        except yaml.YAMLError as exc:
            print("exc")


if __name__ == '__main__':
    pattern_checking()
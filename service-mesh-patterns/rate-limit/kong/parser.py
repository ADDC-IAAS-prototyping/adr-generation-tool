#!/usr/bin/env python

import yaml
import pint

# Create object for generation of pint measurements
ureg = pint.UnitRegistry()

# globals
enteredInterval = 384 # will be user input
CONFIG_INTERVAL = 0*ureg.minute + enteredInterval * ureg.second
CONFIG_RATE = 61 # will be user input

TOO_HIGH = 'TOO MANY REQUESTS ALLOWED FOR INPUT INTERVAL'
TOO_LOW = 'TOO FEW REQUESTS ALLOWED FOR INPUT INTERVAL'
COMPLIANT = 'EVERYTHING IS FINE'

def convertEvenPintMeasureToInt(pintMeasure):
    """ Conversion of pint.UnitRegistry measurement types to ints.
    Should only be done with measures which are natural numbers (rounded floats)
    """
    return int(float(''.join(c for c in str(pintMeasure) if c.isdigit() or c=='.')))

def check_platform(yaml_file):
    """ Simple check from which platform the parsed yaml file comes from
    """
    if hasattr(yaml_file, 'apiVersion'):
        if 'istio' in yaml_file.apiVersion:
            return 'istio'
        elif hasattr(yaml_file, 'plugins'):
            if hasattr(yaml_file.plugins, 'name'):
                if 'rate-limiting' in yaml_file.plugins.name:
                    return 'kong'
        else:
            return None

def update_kong_units(unit, highestUnit):
    """ Will be called while iterating through the config object in a KONG plugin.
    Updates the highestUnit (year > month > day > hour > minute > second) and downs back the previous 
    highest unit to be the second highest unit type (subUnit). This will be relevant if the rate limit 
    interval is configured uneven wrt. highestUnit format (4500s = 1.25h).
    """
    subUnit = highestUnit
    highestUnit = unit
    return highestUnit, subUnit

def get_ureg_unit(passedUnit):
    """ Returns a ureg unit type for a given key word that corresponds to a ureg type.
    """
    for unit in ['second', 'minute', 'hour', 'day', 'month', 'year']:
        if unit == passedUnit:
            return 1*getattr(ureg, unit)
    return None

def collect_kong_properties():
    """ Parse rate limit metrics from KONG plugin yaml and check if the configuration is compliant with 
    user-defined configuration checks (CONFIG_INTERVAL and CONFIG_RATE). For KONG this is particularly 
    complex because of its proprietary format for rate limit configurations.
    """
    
    # Both variables can be filled out and combined to create something like 'source' overrides in Istio
    target = "" # generic named variable for request target (service) 
    source = "" # generic named variable for request source (consumer)

    # get target id
    if 'route' in yaml_file:
        target = yaml_file['route']
    if 'service' in yaml_file:
        target = yaml_file['service']

    # get source id
    if 'consumer' in yaml_file:
        source = yaml_file['consumer']

    # get intervals (in form of time units)
    config = yaml_file['config']

    subUnit = ""
    highestUnit = ""

    # Iterate through the config object in order to check which format rate limits are set
    for unit in ['second', 'minute', 'hour', 'day', 'month', 'year']:
        if unit in config:
            highestUnit, subUnit = update_kong_units(unit, highestUnit)

    # Get two highest rate limits
    subUnitRate = config[subUnit] if subUnit != "" else 0
    highestUnitRate = config[highestUnit] if highestUnit != "" else 0

    highestUnit = get_ureg_unit(highestUnit)
    rest_t_U = 0.0 if CONFIG_INTERVAL % highestUnit == 0 else CONFIG_INTERVAL % highestUnit # Formel B2.1

    def edge_cases_uneven():
        """ Edge cases if the user-defined CONFIG_INTERVAL cannot be divided without a rest wrt. the highest 
        time unit type in the KONG plugin config. For details see formula B1 and B2.1-B2.4.
        """
        interval_down = CONFIG_INTERVAL - rest_t_U
        interval_up = interval_down + 1*ureg.minute

        interval_down_int = convertEvenPintMeasureToInt(interval_down)
        interval_up_int = convertEvenPintMeasureToInt(interval_up)

        kongInputIntervalRate = highestUnitRate * interval_up_int

        print("--------------------------")
        print("interval up: " + str(interval_up))
        print("interval down: " + str(interval_down))
        print("REST_t_U: " + str(rest_t_U))
        print('kongInputIntervalRate: ' + str(kongInputIntervalRate))
        print('highestUnitRate: ' + str(highestUnitRate))
        print("--------------------------")

        if kongInputIntervalRate < CONFIG_RATE:
            return TOO_LOW
        else:
            rest_req = CONFIG_RATE - (interval_down_int * highestUnitRate)
            print("rest_req: " + str(rest_req))
            rest_t_s = 0*ureg.second + rest_t_U
            print('rest_t_s: ' + str(rest_t_s))
            setpoint_kong_subunit_rate = rest_req / convertEvenPintMeasureToInt(rest_t_s)
            print("setpoint is: " + str(setpoint_kong_subunit_rate))
            if subUnitRate == setpoint_kong_subunit_rate:
                return COMPLIANT
            elif subUnitRate < setpoint_kong_subunit_rate:
                returnString = TOO_LOW + '\n' + 'SUBUNIT RATE SHOULD BE ' + str(setpoint_kong_subunit_rate)
                return returnString
            else:
                returnString = TOO_HIGH + '\n' + 'SUBUNIT RATE SHOULD BE ' + str(setpoint_kong_subunit_rate)
                return returnString
        return 0

    def edge_cases_even():
        configIntervalUntyped = convertEvenPintMeasureToInt(CONFIG_INTERVAL) 
        kongInputIntervalRate = configIntervalUntyped * highestUnitRate

        if CONFIG_RATE == kongInputIntervalRate:
            return COMPLIANT
        elif CONFIG_RATE < kongInputIntervalRate:
            return TOO_LOW
        else:
            return TOO_HIGH
        return ""

    if rest_t_U == 0:
        return edge_cases_even()
    else:
        return edge_cases_uneven()

with open("rate_limit_example.yaml", "r") as stream:
    try:
        yaml_file = yaml.safe_load(open("rate_limit_example.yaml", "r"))["plugins"]
    except yaml.YAMLError as exc:
        print(exc)

#print(check_platform(yaml_file))
print(collect_kong_properties())
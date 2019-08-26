#!/usr/bin/env python

import pint

# Create object for generation of pint measurements
ureg = pint.UnitRegistry()

TOO_HIGH = 'TOO MANY REQUESTS ALLOWED FOR INPUT INTERVAL'
TOO_LOW = 'TOO FEW REQUESTS ALLOWED FOR INPUT INTERVAL'
COMPLIANT = 'EVERYTHING IS FINE'

class Parser(object):

    def __init__(self, config_interval, config_rate):
        self.config_interval = 0*ureg.minute + config_interval * ureg.second
        self.config_rate = config_rate

    def update_units(self, unit, highest_unit):
        """Will be called while iterating through the config object in a KONG plugin.
        Updates the highest_unit (year > month > day > hour > minute > second) and downs back the previous 
        highest unit to be the second highest unit type (sub_unit). This will be relevant if the rate limit 
        interval is configured uneven wrt. highest_unit format (4500s = 1.25h).
        """
        sub_unit = highest_unit
        highest_unit = unit
        return highest_unit, sub_unit

    def get_ureg_unit(self, unit_passed):
        """Returns a ureg unit type for a given key word that corresponds to a ureg type.
        """
        for unit in ['second', 'minute', 'hour', 'day', 'month', 'year']:
            if unit == unit_passed:
                return 1*getattr(ureg, unit)
        return None
    
    def convert_even_pint_measure_to_int(self, pint_measure):
        """Conversion of pint.UnitRegistry measurement types to ints.
        Should only be done with measures which are natural numbers (rounded floats)
        """
        return int(float(''.join(c for c in str(pint_measure) if c.isdigit() or c=='.')))

    def edge_cases_even(self, rate_highest_unit):
        """Edge cases if the user-defined CONFIG_INTERVAL can be divided without a rest wrt. the highest 
        time unit type in the KONG plugin config. For details see formula A1-A3.
        """
        config_interval_untyped = self.convert_even_pint_measure_to_int(self.config_interval)
        rate_config_interval_kong = config_interval_untyped * rate_highest_unit

        if self.config_rate == rate_config_interval_kong:
            return COMPLIANT
        elif self.config_rate < rate_config_interval_kong:
            return TOO_LOW
        else:
            return TOO_HIGH
        return ""

    def edge_cases_uneven(self, rest_time_in_highest_unit, rate_highest_unit, rate_sub_unit):
        """Edge cases if the user-defined CONFIG_INTERVAL cannot be divided without a rest wrt. the highest 
        time unit type in the KONG plugin config. For details see formula B1 and B2.1-B2.4.
        """
        interval_down = self.config_interval - rest_time_in_highest_unit
        interval_up = interval_down + 1*ureg.minute

        interval_down_int = self.convert_even_pint_measure_to_int(interval_down)
        interval_up_int = self.convert_even_pint_measure_to_int(interval_up)

        kongInputIntervalRate = rate_highest_unit * interval_up_int

        print("--------------------------")
        print("interval up: " + str(interval_up))
        print("interval down: " + str(interval_down))
        print("rest_time_in_highest_unit: " + str(rest_time_in_highest_unit))
        print('kongInputIntervalRate: ' + str(kongInputIntervalRate))
        print('highestUnitRate: ' + str(rate_highest_unit))
        print("--------------------------")

        if kongInputIntervalRate < self.config_rate:
            return TOO_LOW
        else:
            rest_req = self.config_rate - (interval_down_int * rate_highest_unit)
            print("rest_req: " + str(rest_req))
            rest_time_in_seconds = 0*ureg.second + rest_time_in_highest_unit
            print('rest_time_in_seconds: ' + str(rest_time_in_seconds))
            setpoint_kong_subunit_rate = rest_req / self.convert_even_pint_measure_to_int(rest_time_in_seconds)
            print("setpoint is: " + str(setpoint_kong_subunit_rate))
            if rate_sub_unit == setpoint_kong_subunit_rate:
                return COMPLIANT
            elif rate_sub_unit < setpoint_kong_subunit_rate:
                returnString = TOO_LOW + '\n' + 'SUBUNIT RATE SHOULD BE ' + str(setpoint_kong_subunit_rate)
                return returnString
            else:
                returnString = TOO_HIGH + '\n' + 'SUBUNIT RATE SHOULD BE ' + str(setpoint_kong_subunit_rate)
                return returnString
        return 0

    def check_config(self, config_file):
        """Parse rate limit metrics from KONG plugin yaml and check if the configuration is compliant with 
        user-defined configuration checks (config_interval and CONFIG_RATE). For KONG this is particularly 
        complex because of its proprietary format for rate limit configurations.
        """

        target = ''
        source = ''

        # get target id
        if 'route' in config_file:
            target = config_file['route']
        if 'service' in config_file:
            target = config_file['service']

        # get source id
        if 'consumer' in config_file:
            source = config_file['consumer']

        config_file = config_file['config']

        highest_unit = ''
        sub_unit = ''

        # Iterate through the config object in order to check which format rate limits are set
        for unit in ['second', 'minute', 'hour', 'day', 'month', 'year']:
            if unit in config_file:
                highest_unit, sub_unit = self.update_units(unit, highest_unit)
        
        # Get two highest rate limits
        rate_sub_unit = config_file[sub_unit] if sub_unit != "" else 0
        rate_highest_unit = config_file[highest_unit] if highest_unit != "" else 0

        highest_unit = self.get_ureg_unit(highest_unit)
        rest_time_in_highest_unit = 0.0 if self.config_interval % highest_unit == 0 else self.config_interval % highest_unit # Formel B2.1

        # Execute core functionality
        if rest_time_in_highest_unit == 0:
            return self.edge_cases_even(rate_highest_unit)
        else:
            return self.edge_cases_uneven(rest_time_in_highest_unit, rate_highest_unit, rate_sub_unit)
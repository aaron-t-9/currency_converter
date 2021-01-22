"""
Canadian Currency Converter

Created by Aaron T. and Jasper Z.
"""

import json
import requests


def currency_converter(url: str) -> None:
    """
    Nothing is returned, drives the program.

    Uses a while loop to drive the program and terminates the program if the user enters the letter
    "e". Calls on helper functions to convert the user specified amount to their desired currency_converter

    :param url: A string.
    :precondition: A string containing the url of the API with the currency conversion data.
                   The API must contain the json from www.floatrates.com
    :postcondition: Nothing is returned. Calls on helper functions to convert the user specified
                    amount to their desired currency.
    :return: Nothing is returned.
    """
    currency_keys_list = []
    user_input = ""

    while user_input != 'e':
        response = requests.get(url)    # Updates the currencies everytime the loop is run
        data = json.loads(response.text)
        for key in data.keys():
            currency_keys_list.append(key)

        print("\nCAD to foreign currency converter\nEnter 'e' to quit anytime\n\n")
        user_input = input("Enter amount of CAD to be converted (your value will be rounded to two decimals): ").strip()
        if user_input != 'e':
            try:
                user_input = float(user_input)
            except ValueError:
                print("Invalid input...\n")
                continue
            else:
                other_currency = get_currency_choice(currency_keys_list, data)
                if other_currency:
                    convert_currency(float(user_input), other_currency, data)
                else:
                    continue
        else:
            continue


def get_currency_choice(currency_keys_list: list, data: dict) -> str:
    """Returns a string containing the currency code the user would like to convert.

    Accepts a list of currency keys, and the dictionary containing the json data, accepts user
    input, and returns the three letter code associated with the currency.

    :param currency_keys_list: A list.
    :param data: A dictionary.
    :precondition: The user input should be the integer associated with the currency they would
                   like to convert.
    :precondition currency_keys_list: A list containing all of the three letter currency keys
                                      from the currency json file.
    :precondition data: A dictionary containing the json data from www.floatrates.com. Contains
                        a dictionary of containing the information of the different currencies,
                        including conversion rates relative to CAD.
    :postcondition: Returns a string containing three letter currency code selected by the user.
    :return: A string.
    """
    for currency in currency_keys_list:
        print(f"{currency_keys_list.index(currency) + 1}. {currency} - {data[currency]['name']}")

    try:
        user_currency = input(
            "\nPlease enter the number associated with the currency you would like to convert to: ").strip()
        currency_index = int(user_currency) - 1
        user_currency_code = currency_keys_list[currency_index]
    except (ValueError, IndexError):
        print(f"Invalid number.\n")
        return None
    else:
        return user_currency_code


def convert_currency(user_input: float, other_currency: str, data: dict) -> None:
    """Calculate currency to foreign currency.

    Accepts a string of the user specified foreign currency, and the dictionary containing the
    json data, accepts user input, and returns the three letter code associated with the currency.

    :param user_input: A floating point number.
    :param other_currency: A string.
    :param data: A dictionary.
    :precondition user_input: Must be a floating point number representing the amount that the user
                              would like to convert.
    :precondition other_currency: A string containing the three letter currency code that the
                                  user would like to convert to.
    :precondition data: A dictionary containing the json data from www.floatrates.com. Contains a
                        dictionary of dictionaries the information of the different currencies,
                        including conversion rates relative to CAD.
    :postcondition: Returns a string containing the three letter currency code specified
                    by the user.
    :returns: A string.
    """
    user_input = round(user_input, 2)
    other_currency_rate = data[other_currency]["rate"]
    other_currency_value = round((user_input) * (other_currency_rate),2)
    print(f"\n{user_input} CAD converts into {other_currency_value} {other_currency.upper()}.\n\n")


def main():
    """Execute the program"""
    url = "http://www.floatrates.com/daily/cad.json"
    currency_converter(url)
    print("Terminating currency converter...")


if __name__ == "__main__":
    main()

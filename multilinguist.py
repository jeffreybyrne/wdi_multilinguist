import requests
# import ipdb
from random import randint
import json

class Multilinguist:
  """This class represents a world traveller who knows
  what languages are spoken in each country around the world
  and can cobble together a sentence in most of them
  (but not very well)
  """

  translatr_base_url = "http://bitmakertranslate.herokuapp.com"
  countries_base_url = "https://restcountries.eu/rest/v2/name"
  #{name}?fullText=true
  #?text=The%20total%20is%2020485&to=ja&from=en

  def __init__(self):
    """Initializes the multilinguist's current_lang to 'en'

    Returns
    -------
    Multilinguist
        A new instance of Multilinguist
    """
    self.current_lang = 'en'

  def language_in(self, country_name):
    """Uses the RestCountries API to look up one of the languages
    spoken in a given country

    Parameters
    ----------
    country_name : str
         The full name of a country.

    Returns
    -------
    bool
        2 letter iso639_1 language code.
    """
    params = {'fullText': 'true'}
    response = requests.get(f"{self.countries_base_url}/{country_name}", params=params)
    json_response = json.loads(response.text)
    return json_response[0]['languages'][0]['iso639_1']

  def travel_to(self, country_name):
    """Sets current_lang to one of the languages spoken
    in a given country

    Parameters
    ----------
    country_name : str
        The full name of a country.

    Returns
    -------
    str
        The new value of current_lang as a 2 letter iso639_1 code.
    """
    local_lang = self.language_in(country_name)
    self.current_lang = local_lang
    return self.current_lang

  def say_in_local_language(self, msg):
    """(Roughly) translates msg into current_lang using the Transltr API

    Parameters
    ----------
    msg : str
        A message to be translated.

    Returns
    -------
    str
        A rough translation of msg.
    """
    params = {'text': msg, 'to': self.current_lang, 'from': 'en'}
    response = requests.get(self.translatr_base_url, params=params)
    json_response = json.loads(response.text)
    # print('---')
    # print(json_response)
    # print('---')
    return json_response['translationText']


class MathGenius(Multilinguist):

    def report_total(self, number_list):
        curr_total = 0
        for num in range(0, len(number_list)):
            curr_total += number_list[num]
        return "{} {}".format(self.say_in_local_language("The total is "), str(curr_total))


class QuoteCollector(Multilinguist):
    """This class represents a multilinguist with a collection of quotes
    """
    def __init__(self):
        super().__init__()
        self.quotes = []

    def add_quote(self, new_quote):
        self.quotes.append(new_quote)
        print('hi')

    def say_something_random(self):
        return self.say_in_local_language(self.quotes[randint(0, len(self.quotes)-1)])


jeff = Multilinguist()
print(jeff.current_lang)
# print(jeff.say_in_local_language('hello'))
print(jeff.language_in('CN'))
print(jeff.language_in('RU'))
jeff.travel_to('FR')
print(jeff.current_lang)
print(jeff.say_in_local_language('hello'))
jeff2 = MathGenius()
jeff2.travel_to('FR')
print(jeff2.report_total([23,45,676,34,5778,4,23,5465]))

me = MathGenius()
print(me.report_total([23,45,676,34,5778,4,23,5465])) # The total is 12048
me.travel_to("India")
print(me.report_total([6,3,6,68,455,4,467,57,4,534])) # है को कुल 1604
me.travel_to("Italy")
print(me.report_total([324,245,6,343647,686545])) # È Il totale 1030767

you = QuoteCollector()
you.travel_to("Italy")
you.add_quote("Hello! Today is Saturday.")
print(you.say_something_random())

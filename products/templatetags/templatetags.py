from django import template

import json

register = template.Library()

@register.filter(name="loadJson")
def loadJson(string):
    return json.loads(string)

@register.filter(name="getFromDict")
def getFromDict(dict, value):
    return dict.get(value, "")

@register.filter(name="getWithIndex")
def getWithIndex(items, index):
    return items[index]

@register.filter(name="substract")
def substract(value1, value2):
    return value1 - value2
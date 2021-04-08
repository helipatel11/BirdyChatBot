# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests
from string import Template
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def getResponseFromAPI(departure, destination, date):
    url = 'http://api.aviationstack.com/v1/flights?access_key=ENTER_YOUR_API_KEY'
    response = requests.get(url)
    print(response.status_code)
    json_data = response.json()
    flights = json_data['data']
    print(flights)
    result_flights = []
    for flight in flights:
        if str(flight['departure']['timezone']).find(departure) != -1:
            if str(flight['arrival']['timezone']).find(destination) != -1 and str(date)==flight['flight_date']:
                result_flights.append(flight)
    print(result_flights)
    return result_flights

class ViewFlightIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("viewflight")(handler_input)
    
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        destination_value=slots["destination"].value
        departure_value=slots["departure"].value
        date_value=slots["date"].value
        flights = getResponseFromAPI(destination_value, departure_value, date_value)
        final_str = ""
        for flight in flights:
            url = "www."
            url = url + flight["airline"]["name"].lower().replace(" ", "") + ".com"
            final_str = final_str + "Airline: " + flight["airline"]["name"] + " | " + flight["departure"]["scheduled"] + " | Departure Airport: " + flight["departure"]["airport"] + " | Destination Location: " + destination_value + " | Departure Location: " + departure_value + " | For more information, Go to: " + url 
        
        print(final_str)
        return (
            handler_input.response_builder
            .speak(final_str)
            .response
        )
class AirportLookUpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("airportlookup")(handler_input)
    
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        destination_value=slots["destination"].value
        airport_value=slots["airport"].value
        url = 'http://api.aviationstack.com/v1/flights?access_key=ENTER_YOUR_API_KEY'
        response = requests.get(url)
        print(response.status_code)
        json_data = response.json()
        flights = json_data['data']
        print(flights)
        result_flights = []
        for flight in flights:
            if str(flight['arrival']['timezone']).find(destination_value) != -1:
                if str(flight['departure']['airport']).lower() == airport_value.lower():
                    result_flights.append(flight)
        print(result_flights)
        final_str = ""
        count = 0
        for flight in flights:
            count=count+1
            sd = str(flight["departure"]["scheduled"])
            str1 = sd.replace(':00+00:00', '')
            if count < 3:
                final_str = final_str + flight["flight"]["number"] + " " + flight["airline"]["name"] + " " + str1.replace('T',' ') + 'EST' + ", "
            else:
                final_str = final_str + flight["flight"]["number"] + " " + flight["airline"]["name"] + " " + str1.replace('T',' ' + 'EST'
                break
        print(final_str)
        return (
            handler_input.response_builder
            .speak(final_str)
            .response
        )
def getFlightFromNo(flightNo):
    url = 'http://api.aviationstack.com/v1/flights?access_key=ENTER_YOUR_API_KEY'
    response = requests.get(url)
    print(response.status_code)
    json_data = response.json()
    flights = json_data['data']
    print(flights)
    flight_result = ""
    for flight in flights:
        if flight['flight']['number'] == str(flightnumber_value):
            flight_result = flight
    return flight_result
class ViewFlightStatusIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("flightstatus")(handler_input)
    
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        flightnumber_value=slots["flightnumber"].value
        url = 'http://api.aviationstack.com/v1/flights?access_key=ENTER_YOUR_API_KEY'
        response = requests.get(url)
        print(response.status_code)
        json_data = response.json()
        flights = json_data['data']
        print(flights)
        flight_result = ""
        for flight in flights:
            if flight['flight']['number'] == str(flightnumber_value):
                flight_result = flight["flight_status"]
        if flight_result == "":
            flight_result = "Check your flight number"
        return (
            handler_input.response_builder
            .speak(flight_result)
            .ask("What would you like to do?")
            .response
        )
class ViewFlightDeptInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("flightdepinfo")(handler_input)
    
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        flightnumber_value=slots["flightnumber"].value
        url = 'http://api.aviationstack.com/v1/flights?access_key=ENTER_YOUR_API_KEY'
        response = requests.get(url)
        print(response.status_code)
        json_data = response.json()
        flights = json_data['data']
        print(flights)
        airport = ""
        terminal = ""
        gate = ""
        delay = ""
        for flight in flights:
            if flight['flight']['number'] == str(flightnumber_value):
                airport = str(flight['departure']['airport'])
                terminal = str(flight['departure']['terminal'])
                gate = str(flight['departure']['gate'])
                delay = str(flight['departure']['delay'])
        if terminal == "null" or terminal == "None":
            terminal = "Not available"
        if gate == "null" or gate == "None":
            gate = "Not available"
        if delay == "null" or delay == "None":
            delay = "Not available"
        final_str = "Airport: " + airport + " | Terminal: " + terminal + " | Gate: " + gate + " | Delay: " + delay
        return (
            handler_input.response_builder
            .speak(final_str)
            .ask("What would you like to do?")
            .response
        )

class ViewFlightArrInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("flightarrinfo")(handler_input)
    
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        flightnumber_value=slots["flightnumber"].value
        url = 'http://api.aviationstack.com/v1/flights?access_key=ENTER_YOUR_API_KEY'
        response = requests.get(url)
        print(response.status_code)
        json_data = response.json()
        flights = json_data['data']
        print(flights)
        airport = ""
        terminal = ""
        gate = ""
        delay = ""
        for flight in flights:
            if flight['flight']['number'] == str(flightnumber_value):
                airport = str(flight['arrival']['airport'])
                terminal = str(flight['arrival']['terminal'])
                gate = str(flight['arrival']['gate'])
                delay = str(flight['arrival']['delay'])
        if terminal == "null" or terminal == "None":
            terminal = "Not available"
        if gate == "null" or gate == "None":
            gate = "Not available"
        if delay == "null" or delay == "None":
            delay = "Not available"
        final_str = "Airport: " + airport + " | Terminal: " + terminal + " | Gate: " + gate + " | Delay: " + delay
        #final_str = "abc"
        return (
            handler_input.response_builder
            .speak(final_str)
            .ask("What would you like to do?")
            .response
        )

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, I am Birdy. I can help you to book a flight."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(ViewFlightIntentHandler())
sb.add_request_handler(AirportLookUpIntentHandler())
sb.add_request_handler(ViewFlightStatusIntentHandler())
sb.add_request_handler(ViewFlightDeptInfoIntentHandler())
sb.add_request_handler(ViewFlightArrInfoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

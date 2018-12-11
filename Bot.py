import os
import dialogflow
import random
import string

class Bot:

    def __init__(self, project_id, language_id):
        self.session_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.project_id = project_id
        self.language_code = language_id


    def say(self, text):

        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(self.project_id, self.session_id)
        # print('Session path: {}\n'.format(session))

        text_input = dialogflow.types.TextInput(
            text=text, language_code=self.language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text, response.query_result.intent.display_name

    @property
    def contexts(self):
        contexts_client = dialogflow.ContextsClient()

        session_path = contexts_client.session_path(self.project_id, self.session_id)

        contexts = contexts_client.list_contexts(session_path)

        dict = {}
        for context in contexts:
            for field, value in context.parameters.fields.items():
                if value.string_value:
                    dict[field] = value.string_value
        return dict
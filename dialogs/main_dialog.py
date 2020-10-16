# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory, CardFactory, UserState
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import (
    OAuthPrompt,
    OAuthPromptSettings,
    ConfirmPrompt,
    PromptOptions,
    TextPrompt,
)
from botbuilder.schema import HeroCard, CardImage
from botbuilder.core import     UserState

from dialogs import LogoutDialog
from simple_graph_client import SimpleGraphClient

from config import DefaultConfig
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint

from data_models import WelcomeUserState

class MainDialog(LogoutDialog):
    def __init__(self, connection_name: str, user_state: UserState):
        super(MainDialog, self).__init__(MainDialog.__name__, connection_name)

        self.add_dialog(
            OAuthPrompt(
                OAuthPrompt.__name__,
                OAuthPromptSettings(
                    connection_name=connection_name,
                    text="Please Sign In",
                    title="Sign In",
                    timeout=300000,
                ),
            )
        )

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.prompt_step,
                    self.login_step,
                    self.command_step,
                    self.process_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

        CONFIG = DefaultConfig()
        self.qna_maker = QnAMaker(
            QnAMakerEndpoint(
                knowledge_base_id=CONFIG.QNA_KNOWLEDGEBASE_ID,
                endpoint_key=CONFIG.QNA_ENDPOINT_KEY,
                host=CONFIG.QNA_ENDPOINT_HOST,
            )
        )

        self.user_state = user_state
        self.user_state_accessor = self.user_state.create_property("WelcomeUserState")


    async def prompt_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.begin_dialog(OAuthPrompt.__name__)

    async def login_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Get the state properties from the turn context.
        welcome_user_state = await self.user_state_accessor.get(step_context._turn_context, WelcomeUserState) 

        # Get the token from the previous step. Note that we could also have gotten the
        # token directly from the prompt itself. There is an example of this in the next method.
        if step_context.result and not welcome_user_state.did_welcome_user:
            welcome_user_state.did_welcome_user = True 

            token_response = step_context.result

            client = SimpleGraphClient(token_response.token)
            me_info = await client.get_me()

            await step_context.context.send_activity("You are now logged as {}.".format(me_info['displayName']))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("How can I help?")
                ),
            )
        elif welcome_user_state.did_welcome_user:
            return await step_context.continue_dialog()


        # await step_context.context.send_activity("Login was not successful please try again.")
        # return await step_context.end_dialog()

    async def command_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["command"] = step_context.result

        # Call the prompt again because we need the token. The reasons for this are:
        # 1. If the user is already logged in we do not need to store the token locally in the bot and worry
        #    about refreshing it. We can always just call the prompt again to get the token.
        # 2. We never know how long it will take a user to respond. By the time the
        #    user responds the token may have expired. The user would then be prompted to login again.
        #
        # There is no reason to store the token locally in the bot because we can always just call
        # the OAuth prompt to get the token or get a new token if needed.
        return await step_context.begin_dialog(OAuthPrompt.__name__)

    async def process_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            token_response = step_context.result
            if token_response and token_response.token:
                parts = step_context.values["command"].split(" ")
                command = parts[0]


                results = await self.qna_maker.get_answers(step_context._turn_context)

                if results:
                    await step_context.context.send_activity(results[0].answer)
                else:
                    await step_context.context.send_activity(
                        "Sorry, could not find an answer in the Q and A system."
                    )
        else:
            await step_context.context.send_activity("We couldn't log you in.")

        await step_context.context.send_activity("Type anything to try again.")
        return await step_context.end_dialog()

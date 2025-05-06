import unittest
from unittest.mock import patch, MagicMock
import chatbot


class TestChatFunction(unittest.TestCase):

    @patch("chatbot.st.rerun")
    @patch("chatbot.st.write_stream")
    @patch("chatbot.st.chat_message")
    @patch("chatbot.AzureOpenAI")
    @patch("chatbot.st.chat_input", return_value="Where should I go this summer?")
    @patch("chatbot.st.markdown")
    @patch("chatbot.st.title")
    @patch("chatbot.st.error")
    @patch("chatbot.st.secrets", new=MagicMock(
        OPENAI_API_KEY="fake-key", OPENAI_API_ENDPOINT="https://example.com"
    ))
    def test_chat_full_flow(
        self, mock_error, mock_title, mock_markdown, mock_chat_input,
        mock_azure_openai, mock_chat_message, mock_write_stream, mock_rerun
    ):
        # Mock session state and assistant response
        mock_stream = MagicMock()
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_stream
        mock_azure_openai.return_value = mock_client
        mock_write_stream.return_value = "Try Bali!"

        # Patch session_state
        with patch.dict("chatbot.st.session_state", {}, clear=True):
            chatbot.chat()

            # Check stream call
            mock_client.chat.completions.create.assert_called_once()
            mock_write_stream.assert_called_with(mock_stream)

            # Check messages appended correctly
            messages = chatbot.st.session_state.messages
            self.assertEqual(messages[-2]["role"], "user")
            self.assertEqual(messages[-1]["role"], "assistant")
            self.assertEqual(messages[-1]["content"], "Try Bali!")

            # Ensure no error shown
            mock_error.assert_not_called()

    @patch("chatbot.st.chat_input", return_value=None)
    @patch("chatbot.st.title")
    @patch("chatbot.st.secrets", new=MagicMock(
        OPENAI_API_KEY="fake-key", OPENAI_API_ENDPOINT="https://example.com"
    ))
    def test_chat_no_prompt(self, mock_title, mock_chat_input):
        with patch.dict("chatbot.st.session_state", {}, clear=True):
            chatbot.chat()
            # Prompt is None, so no processing should occur
            self.assertEqual(len(chatbot.st.session_state.messages), 1)  # Only system message

    @patch("chatbot.st.rerun")
    @patch("chatbot.st.chat_message")
    @patch("chatbot.st.write_stream", side_effect=Exception("Simulated error"))
    @patch("chatbot.AzureOpenAI")
    @patch("chatbot.st.chat_input", return_value="Suggest a place")
    @patch("chatbot.st.markdown")
    @patch("chatbot.st.title")
    @patch("chatbot.st.error")
    @patch("chatbot.st.secrets", new=MagicMock(
        OPENAI_API_KEY="fake-key", OPENAI_API_ENDPOINT="https://example.com"
    ))
    def test_chat_handles_exception(
        self, mock_error, mock_title, mock_markdown, mock_chat_input,
        mock_azure_openai, mock_write_stream, mock_chat_message, mock_rerun
    ):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MagicMock()
        mock_azure_openai.return_value = mock_client

        with patch.dict("chatbot.st.session_state", {}, clear=True):
            chatbot.chat()
            mock_error.assert_called_once()

    @patch("chatbot.st.chat_input", return_value=None)
    @patch("chatbot.st.chat_message")
    @patch("chatbot.st.markdown")
    @patch("chatbot.st.title")
    @patch("chatbot.st.secrets", new=MagicMock(
        OPENAI_API_KEY="fake-key", OPENAI_API_ENDPOINT="https://example.com"
    ))
    def test_rendering_past_messages(self, mock_title, mock_markdown, mock_chat_message, mock_chat_input):
        with patch.dict("chatbot.st.session_state", {
            "messages": [
                {"role": "system", "content": "System setup"},
                {"role": "user", "content": "Hi!"},
                {"role": "assistant", "content": "Hello there!"}
            ]
        }, clear=True):
            chatbot.chat()

            # There are 2 messages to render (skips system message)
            self.assertEqual(mock_chat_message.call_count, 2)
            mock_chat_message.assert_any_call("user")
            mock_chat_message.assert_any_call("assistant")

            # Each message content should be displayed
            mock_markdown.assert_any_call("Hi!")
            mock_markdown.assert_any_call("Hello there!")

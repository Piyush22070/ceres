class ApiResponse:
    """
    Helper class to generate standardized API responses for both normal and error messages.
    """

    @staticmethod
    def success(message: str, msg_type: str = "bot") -> dict:
        """
        Returns a dictionary representing a successful/normal response.

        Args:
            message (str): The main message text.
            msg_type (str): Type of message (default: 'bot').

        Returns:
            dict: Dictionary with a single message under 'messages'.
        """
        return {"messages": [{"text": message, "type": msg_type}]}

    @staticmethod
    def error(message: str, msg_type: str = "bot", exception: Exception = None) -> dict:
        """
        Returns a dictionary representing an error response.

        Args:
            message (str): The main error message text.
            msg_type (str): Type of message (default: 'bot').
            exception (Exception, optional): If provided, append exception text.

        Returns:
            dict: Dictionary with a single error message under 'messages'.
        """
        text = message
        if exception:
            text += f": {str(exception)}"
        return {"messages": [{"text": text, "type": msg_type}]}

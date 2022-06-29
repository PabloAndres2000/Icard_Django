from rest_framework.serializers import ValidationError


class ErrorHandler:
    error_list = list()

    def __init__(self):
        self.error_list = list()

    def handler_error(self, field_name: str, error: str) -> None:
        """
        Method to add an error to the list
        """
        self.error_list.append((field_name, error))

    def raise_errors(self) -> ValidationError:
        """
        Method to raise all errors on the list
        """
        return ValidationError({"errors": self.error_list})

    def have_errors(self) -> bool:
        """
        Method to check if the list have errors
        """
        return len(self.error_list) > 0

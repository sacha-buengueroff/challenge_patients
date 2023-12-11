import json
from fastapi import Response


class ResponseMaker:
    SUCCESS_STATUS = "SUCCESS"
    PARTIAL_SUCCESS_STATUS = "PARTIAL SUCCESS"
    FAIL_STATUS = "FAIL"

    @staticmethod
    def _parse_results(results: dict | list | int | str | float = None):
        """
        This is a private static method used to parse the results returned
        from a function.

        Args:
            results (dict | list | int | str | float): The results to be
            parsed. Defaults to None.

        Returns:
            dict: A dictionary with two keys, 'valids' and 'invalids'.

            - The 'valids' key contains a list of valid results, and the
              'invalids' key contains a list of invalid results.

        Raises:
            None
        """
        if not results:
            return {"valids": [], "invalids": []}

        if isinstance(results, dict):
            if "valids" in results.keys() and "invalids" in results.keys():
                if len(results.keys()) == 2:
                    return results
                else:
                    return {
                        "valids": results["valids"],
                        "invalids": results["invalids"],
                    }
            return {"valids": [results], "invalids": []}

        else:
            res = [results] if not isinstance(results, list) else results
            return {"valids": res, "invalids": []}

    @staticmethod
    def format(
        results: dict | list | int | str | float,
        method: str,
    ):
        """
        Formats the results of a request and returns a Response object.

        Args:
            results (dict | list | int | str | float): The results of the
            request to be formatted. Can be a dictionary, a list, or a scalar
            value.

            method (str): The type of operation that was performed on
            the resource (e.g., GET, POST, PUT, DELETE).

        Returns:
            A Response object containing the formatted results, along with
            metadata such as the operation type, status, and endpoint.
        """
        # Parse the results into a standardized format
        results = ResponseMaker._parse_results(results=results)
        if not results:
            status = ResponseMaker.FAIL_STATUS
        else:
            status = (
                ResponseMaker.calc_status(results=results)
                if method != "GET"
                else ResponseMaker.SUCCESS_STATUS
            )

        # Calculate the status code based on the status
        status_code = ResponseMaker.calc_status_code(status=status)

        # Create the content dictionary to be returned in the response
        content = {
            "operation": method.upper(),
            "status": status,
            "results": results,
        }

        # Create and return the Response object
        return Response(
            content=json.dumps(content, default=str),
            status_code=status_code,
            media_type="application/json",
        )

    @staticmethod
    def format_error(error, method: str):
        """
        Format an error response to return to the client.

        Args:
            error: The error object to be formatted.
            method (str): The HTTP method used in the request.

        Returns:
            A Response object containing the formatted error message.
        """
        # Get the content of the error object
        error_content = vars(error)

        # Set the status code for the response
        status_code = error.status_code if "status_code" in vars(error) else 400

        # Create the content for the response
        content = {
            "operation": method.upper(),
            "status": ResponseMaker.FAIL_STATUS,
            "error": {
                "message": error_content.get("message")
                if error_content.get("message")
                else "No message available for current error",
                "description": error_content.get("error_description")
                if error_content.get("error_description")
                else str(error),
            },
        }

        # Add additional fields to the error content if they exist in the error object
        if "method_name" in error_content.keys():
            content["error"]["method_name"] = error_content["method_name"]
        if "parameters" in error_content.keys():
            content["error"]["parameters"] = error_content["parameters"]

        # Return the formatted response
        return Response(
            content=json.dumps(content, default=str),
            status_code=status_code,
            media_type="application/json",
        )

    @staticmethod
    def calc_status(results: dict):
        """
        Calculates the status of an operation based on the given results.

        Args:
            results (dict): A dictionary containing the results of an
            operation, with two keys, 'valids' and 'invalids', each with a
            list of values.

        Returns:
            A string representing the status of the operation. Possible values
            are defined in the ResponseMaker class.
        """
        if len(results["valids"]) > 0 and len(results["invalids"]) == 0:
            return ResponseMaker.SUCCESS_STATUS
        elif len(results["valids"]) > 0 and len(results["invalids"]) > 0:
            return ResponseMaker.PARTIAL_SUCCESS_STATUS
        else:
            return ResponseMaker.FAIL_STATUS

    @staticmethod
    def calc_status_code(status: str):
        """
        Returns the corresponding HTTP status code based on the status
        string.

        Args:
            status (str): The status string to evaluate.

        Returns:
            The corresponding HTTP status code.
        """
        if status == ResponseMaker.SUCCESS_STATUS:
            return 200
        elif status == ResponseMaker.PARTIAL_SUCCESS_STATUS:
            return 202
        elif status == ResponseMaker.FAIL_STATUS:
            return 400

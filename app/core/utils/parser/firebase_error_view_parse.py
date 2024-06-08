class ErrorViewAlertParse:

    case_map = {
        "INVALID_LOGIN_CREDENTIALS": "Credenciales inválidas",
        "INVALID_EMAIL": "Credenciales inválidas",
    }

    @staticmethod
    def get_firebase_view_error(input_str):
        return ErrorViewAlertParse.case_map.get(input_str, "Ocurrió un error en el servidor")

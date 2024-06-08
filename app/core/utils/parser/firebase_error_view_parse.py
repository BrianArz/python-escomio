class FirebaseErrorViewParse:

    case_map = {
        "INVALID_LOGIN_CREDENTIALS": "Credenciales inválidas",
        "INVALID_EMAIL": "Credenciales inválidas",
    }

    @staticmethod
    def view_alert_parse(input_str):
        return FirebaseErrorViewParse.case_map.get(input_str, "Ocurrió un error en el servidor")

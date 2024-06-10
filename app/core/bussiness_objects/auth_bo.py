from flask import current_app

from app.model import CreateAccountRequest, MongoUser, ValidationResult


class AuthBo:

    @staticmethod
    def validate_user(sign_up_data: CreateAccountRequest) -> ValidationResult:
        try:

            if MongoUser.objects(username=sign_up_data.username).first():
                return ValidationResult(is_valid=False, message='El nombre de usuario ya está registrado')

            if MongoUser.objects.filter(escom_id=sign_up_data.escom_id).first():
                return ValidationResult(is_valid=False, message='La boleta ya está registrada')

            return ValidationResult(is_valid=True, message='')

        except Exception as e:
            current_app.logger.error(f'AuthBo - validate user: {str(e)}')
            return ValidationResult(is_valid=False, message=str(e))

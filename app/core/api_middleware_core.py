from app.core.auth_core import get_role_value, role_and_type_checker
from app.shared.db_constants import AppDbValueConstants

check_admin = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
            AppDbValueConstants.ADMINISTRATOR_VALUE,
        )
    ]
)

check_security = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
            AppDbValueConstants.SECURITY_VALUE,
        )
    ]
)

check_security_loader = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.SECURITY_LOADER_KEYCLOAK_VALUE,
            AppDbValueConstants.SECURITY_LOADER_VALUE,
        )
    ]
)

check_loader = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.LOADER_KEYCLOAK_VALUE, AppDbValueConstants.LOADER_VALUE
        )
    ]
)

check_weigher = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
            AppDbValueConstants.WEIGHER_VALUE,
        )
    ]
)

check_manager = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.MANAGER_KEYCLOAK_VALUE,
            AppDbValueConstants.MANAGER_VALUE,
        )
    ]
)

check_client = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.CLIENT_KEYCLOAK_VALUE, AppDbValueConstants.CLIENT_VALUE
        )
    ]
)

check_individual_client = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.CLIENT_KEYCLOAK_VALUE, AppDbValueConstants.CLIENT_VALUE
        )
    ],
    required_user_type=get_role_value(
        AppDbValueConstants.INDIVIDUAL_KEYCLOAK_VALUE,
        AppDbValueConstants.INDIVIDUAL_VALUE,
    ),
)

check_legal_client = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.CLIENT_KEYCLOAK_VALUE, AppDbValueConstants.CLIENT_VALUE
        )
    ],
    required_user_type=get_role_value(
        AppDbValueConstants.LEGAL_KEYCLOAK_VALUE, AppDbValueConstants.LEGAL_VALUE
    ),
)

check_admin_and_client = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
            AppDbValueConstants.ADMINISTRATOR_VALUE,
        ),
        get_role_value(
            AppDbValueConstants.CLIENT_KEYCLOAK_VALUE, AppDbValueConstants.CLIENT_VALUE
        ),
    ]
)

check_admin_and_employee = role_and_type_checker(
    [
        get_role_value(
            AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
            AppDbValueConstants.ADMINISTRATOR_VALUE,
        ),
        get_role_value(
            AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
            AppDbValueConstants.SECURITY_VALUE,
        ),
        get_role_value(
            AppDbValueConstants.SECURITY_LOADER_KEYCLOAK_VALUE,
            AppDbValueConstants.SECURITY_LOADER_VALUE,
        ),
        get_role_value(
            AppDbValueConstants.LOADER_KEYCLOAK_VALUE, AppDbValueConstants.LOADER_VALUE
        ),
        get_role_value(
            AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
            AppDbValueConstants.WEIGHER_VALUE,
        ),
        get_role_value(
            AppDbValueConstants.MANAGER_KEYCLOAK_VALUE,
            AppDbValueConstants.MANAGER_VALUE,
        ),
    ]
)

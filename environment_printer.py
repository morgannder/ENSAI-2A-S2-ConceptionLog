import os


class EnvironmentPrinter:
    SENSITIVE_KEYWORDS = {
        "password",
        "pwd",
        "jeton",
        "token",
        "secret",
        "key",
        "cle",
        "mdp",
        "motdepasse",
    }

    @classmethod
    def est_senssible(cls, variable_name: str) -> bool:
        """
        Détermine si le nom d'une variable d'environnement
        contient un mot-clé sensible.
        """
        name_lower = variable_name.lower()
        return any(keyword in name_lower for keyword in cls.SENSITIVE_KEYWORDS)

    @classmethod
    def print_environment_variables(cls) -> None:
        """
        Affiche toutes les variables d'environnement.
        Les valeurs des variables sensibles sont masquées.
        """
        for key, value in os.environ.items():
            if cls.est_senssible(key):
                print(f"{key}=****")
            else:
                print(f"{key}={value}")

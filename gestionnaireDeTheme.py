from copy import deepcopy
import json
import pathlib
import re

from typing import Iterator


class GestionnaireDeTheme:
    """
    Classe gérant les themes. N'est pas sense être instance par l'utilisateur en dehors de ce fichier.
    Stoque le theme actuel.
    """
    def __init__(self, nom:str="defaut") -> None:
        self.nom: str
        self.fond: str
        self.billes: list[str]

        self._dossier: str = "themes"
        self._default: str = "defaut"

        self.charge_theme(nom)



    def is_color(self, s: str) -> bool:
        """Retourne vrai si la couleur est un code HEX (#RRGGBB)"""
        return re.match("\\A#[0-9a-f]{6}\\Z", s, re.IGNORECASE) != None


    def charge_theme(self, nom: str) -> None:
        """Charge un theme"""        
        path = f"{self._dossier}/{nom}.json"
        content = {}
        try:
            # lecture du fichier
            with open(path) as file: content = json.load(file)

            # conformité des champs
            assert self.is_color(content["fond"]), "couleur de fond invalide"
            assert type(content["billes"]) == list and len(content["billes"]) == 10, "champs billes invalide"
            for c in content["billes"]:
                assert self.is_color(c), "couleurs de billes invalide"

            # changement du theme
            self.nom = nom
            self.fond = content["fond"]
            self.billes = content["billes"]

        # Si il y a un probleme lors de la lecture du theme, quelqu'il soit
        except Exception as e:
            if(nom == self._default):
                print(f"Le thème par defaut n'a pas pu être charge ({e}). Regénération du theme par défault")
                self.regenere_theme_defaut()
            else:
                print(f"Le thème '{nom}' n'a pas pu être charge ({e}). Chargement du thème par defaut")
            self.charge_theme(self._default)


    def iter_themes(self) -> Iterator[str]:
        """Renvoie le nom de tous les themes disponibles"""
        path = pathlib.Path(self._dossier)
        for theme in path.glob('*.json'):
            yield theme.name.removesuffix(".json")


    def regenere_theme_defaut(self):
        """Regenère le theme par defaut si le fichier a été perdu ou modifié"""
        with open(f"{self._dossier}/{self._default}.json", "w") as file:
            json.dump("""
{
    "fond": "#a2d1f7",
    "billes": [
        "#6f33a0",
        "#8601d3",
        "#df0100",
        "#dd6000",
        "#db9400",
        "#d6d300",
        "#02e451",
        "#02d9d9",
        "#028eda",
        "#0252db"
    ]
}"""
                , file)
            
theme = GestionnaireDeTheme()
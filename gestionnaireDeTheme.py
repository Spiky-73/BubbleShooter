import json
import pathlib
import re

from pyparsing import Iterator

dossier: str = "themes"

fond: str
billes: list[str]

_default = "defaut"

def is_color(s: str) -> bool:
    """Retourne vrai si la couleur est un code HEX (#RRGGBB)"""
    return re.match("\\A#[0-9a-f]{6}\\Z", s, re.IGNORECASE) != None


def charge_theme(theme: str) -> None:
    """Charge un theme"""
    global fond, billes # les variables a changer
    
    path = f"{dossier}/{theme}.json"
    content = {}
    try:
        # lecture du fichier
        with open(path) as file: content = json.load(file)

        # conformité des champs
        assert is_color(content["fond"]), "couleur de fond invalide"
        assert type(content["billes"]) == list and len(content["billes"]) == 10, "champs billes invalide"
        for c in content["billes"]:
            assert is_color(c), "couleurs de billes invalide"

        # changement du theme
        nom = theme
        fond = content["fond"]
        billes = content["billes"]

    # Si il y a un probleme lors de la lecture du theme, quelqu'il soit
    except Exception as e:
        if(theme == _default):
            print(f"Le thème par defaut n'a pas pu être charge ({e}). Regénération du theme par défault")
            regenere_theme_defaut()
        else:
            print(f"Le thème '{theme}' n'a pas pu être charge ({e}). Chargement du thème par defaut")
        charge_theme(_default)


def iter_themes() -> Iterator[str]:
    """Renvoie le nom de tous les themes disponibles"""
    path = pathlib.Path(dossier)
    for theme in path.glob('*.json'):
        yield theme.name.removesuffix(".json")


def regenere_theme_defaut():
    """Regenère le theme par defaut si le fichier a été perdu ou modifié"""
    with open(f"{dossier}/{_default}.json", "w") as file:
        file.write("""
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
    )

charge_theme(_default)
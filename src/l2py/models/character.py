
"""Модели для персонажей."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CharacterInfo:
    """Информация о персонаже.

    Attributes:
        name: Имя персонажа.
        race: Раса (0=Human, 1=Elf, 2=Dark Elf, 3=Orc, 4=Dwarf, 5=Kamael).
        class_id: ID класса.
        level: Уровень.
        sex: Пол (0=Male, 1=Female).
        x: Координата X.
        y: Координата Y.
        z: Координата Z.
        hp: Текущее HP.
        mp: Текущее MP.
        max_hp: Максимальное HP.
        max_mp: Максимальное MP.
        sp: Очки умения (Skill Points).
        exp: Опыт.
        session_id: Сессионный ID.
        clan_id: ID клана.
        object_id: Object ID персонажа.
        karma: Карма.
        pk_kills: Количество PK убийств.
        pvp_kills: Количество PvP убийств.
        hair_style: Стиль волос.
        hair_color: Цвет волос.
        face: Лицо.
        vitality: Очки витальности.
        active: Активен ли персонаж.
    """

    name: str
    race: int
    class_id: int
    level: int
    sex: int
    x: int = 0
    y: int = 0
    z: int = 0
    hp: float = 0.0
    mp: float = 0.0
    max_hp: float = 0.0
    max_mp: float = 0.0
    sp: int = 0
    exp: int = 0
    session_id: int = 0
    clan_id: int = 0
    object_id: int = 0
    karma: int = 0
    pk_kills: int = 0
    pvp_kills: int = 0
    hair_style: int = 0
    hair_color: int = 0
    face: int = 0
    vitality: int = 0
    active: bool = False


__all__ = ["CharacterInfo"]

# -*- coding: utf-8 -*-
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


__all__ = ["CharacterInfo"]

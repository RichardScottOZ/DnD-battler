from ..dice import AbilityDie, Dice, SkillRoll, AttackRoll
from ..creature_properties.proficiency import Proficiency
from ..creature_properties.armor import Armor
from ..creature_properties.size import Size
from ..log import log

class CreatureBase:
    # inherited by utils

    ability_names = ['str', 'dex', 'con', 'wis', 'int', 'cha']
    log = log

    def __init__(self):
        self.name = 'unnamed'
        self.base = 'none'    # human bandit
        self.type = 'unknown' # aberation, humanoid
        self.size = Size('medium')
        self.arena = None
        self.level = 1
        self.xp = 0
        # proficiency
        # self.proficiency.bonus is dynamic based on proficiency.level + proficiency.modifier
        self.proficiency = Proficiency(0, 0)
        # hits
        self.hp = 4  # commoner.1
        self.starting_hp = 4
        self.hit_die = Dice(8, 0)
        #Ability
        self.able = 1  # has abilities. if nothing at all is provided it goes to zero. This is for rocks...
        self.str = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.dex = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.con = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.wis = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.int = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.cha = AbilityDie(bonus=0, proficiency=self.proficiency)
        # AC
        self.armor = Armor(ability_dice=[self.dex], bonus=0)
        # other
        self.initiative = SkillRoll(self.dex, modifier=0, success_on_crit=False)
        self.attacks = [AttackRoll(name='club', ability_die=self.str, damage_dice=Dice(4,0), modifier=0)]
        self.alt_attack = {}
        self.alignment = 'undeclared'
        self.concentrating = 0
        self.spellcasting_ability_name = None
        self.starting_healing_spells = 0
        self.healing_spells = self.starting_healing_spells
        self.healing = None  # Normally dice object
        # internal stuff
        self.tally = {'damage': 0, 'hits': 0, 'dead': 0, 'misses': 0, 'battles': 0, 'rounds': 0, 'hp': 0,
                      'healing_spells': 0}
        self.copy_index = 1
        self.condition = 'normal'
        self.dodge = 0
        self.temp = 0
        self.buff_spells = 0
        self.conc_fx = None
        self.cr = 0
        self.custom = []

    @property
    def abilities(self):
        """
        A fix to compensate how abilities are handled.
        Now they have their own attribute which is a die. With score and temp_modifier as extras

        :return:
        """
        return {n: getattr(self, n) for n in self.ability_names}

    @property
    def hurtful(self):
        # this is the average damage it can do. But omits if it hits or not...
        return sum([roll.damage_dice.mean() for roll in self.attacks])

    ac = property(lambda self: self.armor.get_ac(), lambda self, value: self.armor.set_ac(value))

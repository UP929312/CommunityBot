import discord
from discord.ext import commands
import re  # For removing colour codes

from parse_profile import get_profile_data

from utils import error, clean
from extract_ids import extract_nbt_dicts
from menus import generate_option_picker, generate_static_preset_menu

NUMBERS = [":one:", ":two:", ":three:", ":four:", ":five:"]#, ":six:", ":seven:", ":eight:", ":nine:"]

gemstone_slots = ['ASPECT_OF_THE_END', 'ASPECT_OF_THE_VOID', 'ZOMBIE_SWORD', 'ORNATE_ZOMBIE_SWORD', 'REAPER_SWORD', 'POOCH_SWORD', 'AXE_OF_THE_SHREDDED', 'YETI_SWORD', 'MIDAS_SWORD', 'DAEDALUS_AXE', 'ASPECT_OF_THE_DRAGON', 'STARRED_BONZO_STAFF', 'BONZO_STAFF', 'BAT_WAND', 'STARRED_STONE_BLADE', 'STONE_BLADE', 'ICE_SPRAY_WAND', 'LIVID_DAGGER', 'STARRED_SHADOW_FURY', 'SHADOW_FURY', 'FLOWER_OF_TRUTH', 'GIANTS_SWORD', 'TITANIUM_DRILL_2', 'TITANIUM_DRILL_3', 'GEMSTONE_DRILL_3', 'BLAZE_ROD', 'MASTIFF_HELMET', 'PERFECT_AMBER_GEM', 'SHARK_SCALE_BOOTS', 'SUPERIOR_DRAGON_BOOTS', 'STARRED_ADAPTIVE_HELMET', 'ADAPTIVE_HELMET', 'STARRED_SHADOW_ASSASSIN_BOOTS', 'SHADOW_ASSASSIN_BOOTS', 'NECROMANCER_LORD_BOOTS', 'SORROW_BOOTS']
dungeonizable_items = ['SOUL_WHIP', 'JERRY_STAFF', 'CRYPT_WITHERLORD_SWORD', 'BONZO_STAFF', 'BONZO_MASK', 'STONE_BLADE', 'ADAPTIVE_HELMET', 'ADAPTIVE_CHESTPLATE', 'ADAPTIVE_LEGGINGS', 'ADAPTIVE_BOOTS', 'SILENT_DEATH', 'CONJURING_SWORD', 'SPIRIT_SWORD', 'ITEM_SPIRIT_BOW', 'THORNS_BOOTS', 'SPIRIT_MASK', 'BONE_BOOMERANG', 'BAT_WAND', 'LAST_BREATH', 'SHADOW_ASSASSIN_HELMET', 'SHADOW_ASSASSIN_CHESTPLATE', 'SHADOW_ASSASSIN_LEGGINGS', 'SHADOW_ASSASSIN_BOOTS', 'SHADOW_FURY', 'LIVID_DAGGER', 'FLOWER_OF_TRUTH', 'FEL_SWORD', 'WITHER_CLOAK', 'PRECURSOR_EYE', 'GIANTS_SWORD', 'NECROMANCER_LORD_HELMET', 'NECROMANCER_LORD_CHESTPLATE', 'NECROMANCER_LORD_LEGGINGS', 'NECROMANCER_LORD_BOOTS', 'NECROMANCER_SWORD', 'NECRON_BLADE', 'HYPERION', 'VALKYRIE', 'SCYLLA', 'ASTRAEA', 'WITHER_HELMET', 'WITHER_CHESTPLATE', 'WITHER_LEGGINGS', 'WITHER_BOOTS', 'TANK_WITHER_HELMET', 'TANK_WITHER_CHESTPLATE', 'TANK_WITHER_LEGGINGS', 'TANK_WITHER_BOOTS', 'SPEED_WITHER_HELMET', 'SPEED_WITHER_CHESTPLATE', 'SPEED_WITHER_LEGGINGS', 'SPEED_WITHER_BOOTS', 'WISE_WITHER_HELMET', 'WISE_WITHER_CHESTPLATE', 'WISE_WITHER_LEGGINGS', 'WISE_WITHER_BOOTS', 'POWER_WITHER_HELMET', 'POWER_WITHER_CHESTPLATE', 'POWER_WITHER_LEGGINGS', 'POWER_WITHER_BOOTS', 'RUNAANS_BOW', 'LEAPING_SWORD', 'SILK_EDGE_SWORD', 'SPIDER_HAT', 'SPIDER_BOOTS', 'MOSQUITO_BOW', 'TARANTULA_HELMET', 'TARANTULA_CHESTPLATE', 'TARANTULA_LEGGINGS', 'TARANTULA_BOOTS', 'SCORPION_BOW', 'PHANTOM_ROD', 'WEREWOLF_HELMET', 'WEREWOLF_CHESTPLATE', 'WEREWOLF_LEGGINGS', 'WEREWOLF_BOOTS', 'PIGMAN_SWORD', 'UNDEAD_SWORD', 'ZOMBIE_SWORD', 'ORNATE_ZOMBIE_SWORD', 'FLORID_ZOMBIE_SWORD', 'SKELETON_HAT', 'ZOMBIE_HAT', 'ZOMBIE_HEART', 'ZOMBIE_CHESTPLATE', 'ZOMBIE_LEGGINGS', 'ZOMBIE_BOOTS', 'SKELETON_HELMET', 'MACHINE_GUN_BOW', 'CRYPT_BOW', 'CRYPT_DREADLORD_SWORD', 'CRYPT_WITHERLORD_HELMET', 'CRYPT_WITHERLORD_CHESTPLATE', 'CRYPT_WITHERLORD_LEGGINGS', 'CRYPT_WITHERLORD_BOOTS', 'SKELETON_GRUNT_HELMET', 'SKELETON_GRUNT_CHESTPLATE', 'SKELETON_GRUNT_LEGGINGS', 'SKELETON_GRUNT_BOOTS', 'SNIPER_BOW', 'SNIPER_HELMET', 'ROTTEN_HELMET', 'ROTTEN_CHESTPLATE', 'ROTTEN_LEGGINGS', 'ROTTEN_BOOTS', 'UNDEAD_BOW', 'STONE_CHESTPLATE', 'MENDER_HELMET', 'DARK_GOGGLES', 'HEAVY_HELMET', 'HEAVY_CHESTPLATE', 'HEAVY_LEGGINGS', 'HEAVY_BOOTS', 'SUPER_HEAVY_HELMET', 'SUPER_HEAVY_CHESTPLATE', 'SUPER_HEAVY_LEGGINGS', 'SUPER_HEAVY_BOOTS', 'STINGER_BOW', 'BOUNCY_HELMET', 'BOUNCY_CHESTPLATE', 'BOUNCY_LEGGINGS', 'BOUNCY_BOOTS', 'SKELETON_MASTER_HELMET', 'SKELETON_MASTER_CHESTPLATE', 'SKELETON_MASTER_LEGGINGS', 'SKELETON_MASTER_BOOTS', 'SKELETON_SOLDIER_HELMET', 'SKELETON_SOLDIER_CHESTPLATE', 'SKELETON_SOLDIER_LEGGINGS', 'SKELETON_SOLDIER_BOOTS', 'ZOMBIE_SOLDIER_HELMET', 'ZOMBIE_SOLDIER_CHESTPLATE', 'ZOMBIE_SOLDIER_LEGGINGS', 'ZOMBIE_SOLDIER_BOOTS', 'ZOMBIE_KNIGHT_HELMET', 'ZOMBIE_KNIGHT_CHESTPLATE', 'ZOMBIE_KNIGHT_LEGGINGS', 'ZOMBIE_KNIGHT_BOOTS', 'ZOMBIE_KNIGHT_SWORD', 'ZOMBIE_COMMANDER_HELMET', 'ZOMBIE_COMMANDER_CHESTPLATE', 'ZOMBIE_COMMANDER_LEGGINGS', 'ZOMBIE_COMMANDER_BOOTS', 'ZOMBIE_COMMANDER_WHIP', 'ZOMBIE_LORD_HELMET', 'ZOMBIE_LORD_CHESTPLATE', 'ZOMBIE_LORD_LEGGINGS', 'ZOMBIE_LORD_BOOTS', 'SKELETON_LORD_HELMET', 'SKELETON_LORD_CHESTPLATE', 'SKELETON_LORD_LEGGINGS', 'SKELETON_LORD_BOOTS', 'SKELETOR_HELMET', 'SKELETOR_CHESTPLATE', 'SKELETOR_LEGGINGS', 'SKELETOR_BOOTS', 'ZOMBIE_SOLDIER_CUTLASS', 'METAL_CHESTPLATE', 'MENDER_FEDORA', 'SHADOW_GOGGLES', 'SUPER_UNDEAD_BOW', 'EARTH_SHARD', 'STEEL_CHESTPLATE', 'MENDER_CROWN', 'WITHER_GOGGLES', 'DEATH_BOW', 'CRYSTALLIZED_HEART', 'REVIVED_HEART', 'REAPER_MASK', 'REAPER_SCYTHE', 'REVENANT_SWORD', 'REAPER_SWORD', 'AXE_OF_THE_SHREDDED', 'ASPECT_OF_THE_DRAGON', 'YOUNG_DRAGON_HELMET', 'YOUNG_DRAGON_CHESTPLATE', 'YOUNG_DRAGON_LEGGINGS', 'YOUNG_DRAGON_BOOTS', 'OLD_DRAGON_HELMET', 'OLD_DRAGON_CHESTPLATE', 'OLD_DRAGON_LEGGINGS', 'OLD_DRAGON_BOOTS', 'STRONG_DRAGON_HELMET', 'STRONG_DRAGON_CHESTPLATE', 'STRONG_DRAGON_LEGGINGS', 'STRONG_DRAGON_BOOTS', 'PROTECTOR_DRAGON_HELMET', 'PROTECTOR_DRAGON_CHESTPLATE', 'PROTECTOR_DRAGON_LEGGINGS', 'PROTECTOR_DRAGON_BOOTS', 'WISE_DRAGON_HELMET', 'WISE_DRAGON_CHESTPLATE', 'WISE_DRAGON_LEGGINGS', 'WISE_DRAGON_BOOTS', 'UNSTABLE_DRAGON_HELMET', 'UNSTABLE_DRAGON_CHESTPLATE', 'UNSTABLE_DRAGON_LEGGINGS', 'UNSTABLE_DRAGON_BOOTS', 'SUPERIOR_DRAGON_HELMET', 'SUPERIOR_DRAGON_CHESTPLATE', 'SUPERIOR_DRAGON_LEGGINGS', 'SUPERIOR_DRAGON_BOOTS', 'HOLY_DRAGON_HELMET', 'HOLY_DRAGON_CHESTPLATE', 'HOLY_DRAGON_LEGGINGS', 'HOLY_DRAGON_BOOTS', 'TERMINATOR', 'SINSEEKER_SCYTHE', 'JUJU_SHORTBOW', 'MIDAS_STAFF', 'ROGUE_SWORD', 'MIDAS_SWORD', 'SUPER_CLEAVER', 'HYPER_CLEAVER', 'GIANT_CLEAVER', 'GOLD_BONZO_HEAD', 'GOLD_SCARF_HEAD', 'GOLD_PROFESSOR_HEAD', 'GOLD_THORN_HEAD', 'GOLD_LIVID_HEAD', 'GOLD_SADAN_HEAD', 'GOLD_NECRON_HEAD', 'HARDENED_DIAMOND_HELMET', 'HARDENED_DIAMOND_CHESTPLATE', 'HARDENED_DIAMOND_LEGGINGS', 'HARDENED_DIAMOND_BOOTS', 'PERFECT_HELMET_1', 'PERFECT_CHESTPLATE_1', 'PERFECT_LEGGINGS_1', 'PERFECT_BOOTS_1', 'DIAMOND_BONZO_HEAD', 'DIAMOND_SCARF_HEAD', 'DIAMOND_PROFESSOR_HEAD', 'DIAMOND_THORN_HEAD', 'DIAMOND_LIVID_HEAD', 'DIAMOND_SADAN_HEAD', 'DIAMOND_NECRON_HEAD', 'YETI_SWORD', 'FROZEN_BLAZE_HELMET', 'FROZEN_BLAZE_CHESTPLATE', 'FROZEN_BLAZE_LEGGINGS', 'FROZEN_BLAZE_BOOTS', 'FROZEN_SCYTHE', 'ICE_SPRAY_WAND']
starrable_items = ['BONZO_STAFF', 'STONE_BLADE', 'SHADOW_FURY', 'ADAPTIVE_HELMET', 'SHADOW_ASSASSIN_BOOTS']

#emoji_list = ['<:misc:854801277489774613>', '<:paper:873158778487443486>', '<:enchantments:854756289010728970>', '<:power_ability_scroll:869701966173974538>']
emoji_list = ['<:misc:854801277489774613>', '<:tier_1_enchants:884441670291189844> ', '<:tier_2_enchants:884441703203864647> ', '<:tier_3_enchants:884441720182423633>']
#emoji_list = ['<:misc:854801277489774613>', '', '', '']
emoji_list = ['<:misc:854801277489774613>', '<:tier_1_enchants:884755357379997748> ', '<:tier_2_enchants:884755365470826536> ', '<:tier_3_enchants:884755490066817034>']

tier_1_sword_enchs = {
    "critical": 5,
    "cubism": 5,
    "ender_slayer": 5,
    "execute": 5,
    #"prosecute": 5,
    "experience": 3,
    "first_strike": 4,
    "triple_strike": 4,
    "giant_killer": 5,
    #"titan_killer": 6,
    "impaling": 3,
    "lethality": 6,
    "life_steal": 4,
    #"syphon": 4,
    #"mana_steal": 3,
    "looting": 4,
    "luck": 6,
    "scavenger": 4,
    "sharpness": 5,
    "smite": 6,
    #"bane_of_arthropods": 6,
    "telekinesis": 1,
    "thunderlord": 6,
    "thunderbolt": 5,
    "vampirism": 5,
    "venomous": 5,
}

tier_2_sword_enchs = {
    "critical": 6,
    "cubism": 5,
    "ender_slayer": 6,
    "execute": 5,
    #"prosecute": 5,
    "experience": 4,
    "first_strike": 4,
    #"triple_strike": 4,
    "giant_killer": 6,
    #"titan_killer": 6,
    "impaling": 3,
    "lethality": 6,
    "life_steal": 4,
    #"syphon": 4,
    #"mana_steal": 3,
    #"looting": 4,
    #"luck": 6,
    "scavenger": 4,
    "sharpness": 6,
    "smite": 7,
    #"bane_of_arthropods": 6,
    "telekinesis": 1,
    "thunderlord": 6,
    "thunderbolt": 5,
    "vampirism": 6,
    "venomous": 5,
}

tier_3_sword_enchs = {
    "cleave": 6,
    "critical": 7,
    "cubism": 6,
    "dragon_hunter": 5,
    "ender_slayer": 7,
    "execute": 6,
    #"prosecute": 6,
    "experience": 4,
    "first_strike": 5,
    #"triple_strike": 5,
    "giant_killer": 7,
    #"titan_killer": 7,
    "impaling": 3,
    "lethality": 6,
    "life_steal": 5,
    #"syphon": 5,
    #"mana_steal": 3,
    "looting": 5,
    "luck": 7,
    "scavenger": 5,
    "sharpness": 7,
    "smite": 7,
    #"bane_of_arthropods": 7,
    "telekinesis": 1,
    "thunderlord": 6,
    "thunderbolt": 6,
    "vampirism": 6,
    "venomous": 6,
    "vicious": 5,
}

sword_enchant_lists = (tier_1_sword_enchs, tier_2_sword_enchs, tier_3_sword_enchs)

class maxer_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['max'])
    async def maxer(self, ctx, username=None):
        
        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        inventory_string = player_data["inv_contents"]["data"]
        inventory_decoded = extract_nbt_dicts(inventory_string)
        inventory_with_lore = [x for x in inventory_decoded if "display" in x and "Lore" in x["display"]]
        
        swords = [x for x in inventory_with_lore if "SWORD" in x["display"]["Lore"][-1]][:5]
        if not swords:
            return await error(ctx, "Error, no swords found", "The bot looked through your inventory and couldn't find any swords, try putting some in!")

        description_list = [f"{NUMBERS[i]} {re.sub('§.', '', x['display']['Name'])}" for i, x in enumerate(swords)]
        
        embed = discord.Embed(title=f"{username}'s Swords", description="\n".join(description_list), url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

        ######################################################################################################################
        option_picked, view_object = await generate_option_picker(ctx, embed, len(swords))
        if option_picked is None:
            return

        item_to_max = swords[option_picked-1]
        ######################################################################################################################        
        extras = item_to_max["ExtraAttributes"]
        internal_name = extras["id"]
        
        missing_elements = []

        if not extras.get("rarity_upgrades", False):
            missing_elements.append("Missing a **Recombobulator**!")
            
        if (hot_potato_books := extras.get("hot_potato_count", 0)) < 15:
            if hot_potato_books < 10:
                missing_elements.append(f"Missing {10-hot_potato_books} **Hot** and 5 **Fuming potato books**!")
            else:
                missing_elements.append(f"Missing {15-hot_potato_books} **Fuming potato books**!")
                
        if extras.get("modifier", None) != "fabled":
            missing_elements.append(f"Missing the **Fabled** reforge!")
        if not extras.get("art_of_war_count", 0):
            missing_elements.append(f"Missing an **Art of War** book!")

        if internal_name in dungeonizable_items and (stars := extras.get("dungeon_item_level", 0)) < 9:
            if stars < 5:
                missing_elements.append(f"Missing {5-stars} **Dungeons Stars** and 4 **Master Stars**!")
            else:
                missing_elements.append(f"Missing {9-stars} **Master Stars**!")

        if internal_name in gemstone_slots:
            if extras.get("gems", {}) == {}:
                missing_elements.append(f"Missing a **Gemstone**!")

        if internal_name in starrable_items:  # If it could have been upgraded
            missing_elements.append(f"Missing **8 Livid Fragments**!")
            
        if internal_name in ["HYPERION", "ASTRAEA", "SCYLLA", "VALKYRIE"]:
            if not extras.get("ability_scroll", False):
                missing_elements.append(f"Missing an **Necron's Blade Scroll**!")
            if not extras.get("ability_scrolls_value", False):
                missing_elements.append(f"Missing a **Power Scroll!")

        if internal_name == "ASPECT_OF_THE_VOID" and not extras.get("ethermerge", False):
            missing_elements.append(f"Missing an **Etherwarp Merger and Conduit**!")
        if internal_name == "ASPECT_OF_THE_JERRY" and not extras.get("wood_singularity_count", False):
            missing_elements.append(f"Missing a **Wood Singularity**!")
            
        if internal_name in ["ASPECT_OF_THE_VOID", "ASPECT_OF_THE_END"] and (tuners := extras.get('tuned_transmission', 0)) < 3:
            missing_elements.append(f"Missing {3-tuners} **Transmission Tuners**!")

        ####################################################
        description = "\n".join(missing_elements) if missing_elements else "The base attributes for this item are already maxed!"

        embed = discord.Embed(title=f"{username}'s Sword", description=description, url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

        list_of_embeds = [embed,]

        for i, enchant_dict in enumerate(sword_enchant_lists):
            missing_enchants = []
            # All the required enchantments
            for key, value in enchant_dict.items():
                # All the ones the player has
                for enchantment, level in extras.get("enchantments", {}).items():
                    # If they have it, break (So the no break doesn't trigger)
                    if key==enchantment and level >= value:
                        continue
                # If we don't skip to the next enchantment, they don't have it, so add it as missing
                missing_enchants.append(f"➥ {clean(key)} - {value}")

            description = "Enchantments missing:\n"+"\n".join(missing_enchants)

            embed = discord.Embed(title=f"{username}'s Sword, Tier {i+1} Enchantments", description=description, url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
            embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

            list_of_embeds.append(embed)
        ########################################################################################################
        await generate_static_preset_menu(ctx, list_of_embeds, emoji_list, message_object=view_object.message)

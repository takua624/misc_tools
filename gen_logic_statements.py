from  numpy.random import randint as ri
import random
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
import re
import numpy as np
import textwrap
from itertools import permutations

def negate_var(var_str):
	var_split = var_str.split(" ")
	if len(var_split)==1:
		return "not "+var_str
	if (len(var_split)>=2):
		if (var_split[0]=="not"):
			return " ".join(var_split[1:])
		if (var_split[0]=="both"):
			var1 = var_str.split("both ")[1].split(" and ")[0]
			var2 = var_str.split("both ")[1].split(" and ")[1]
			return "either "+negate_var(var1)+ " or "+negate_var(var2)
		if (var_split[0]=="either"):
			var1 = var_str.split("either ")[1].split(" or ")[0]
			var2 = var_str.split("either ")[1].split(" or ")[1]
			return "both "+negate_var(var1)+ " and "+negate_var(var2)
	return

def exchange_position(var_str):
	# var_str: in the form of "both (not) X and (not) Y" or "either (not) X or (not) Y"
	have_a_not = False
	if var_str.split(" ")[0]=="not":
		var_str = negate_var(var_str)
		have_a_not = True
	if len(var_str.split("both "))>1:
		var1 = var_str.split("both ")[1].split(" and ")[0]
		var2 = var_str.split("both ")[1].split(" and ")[1]
		return "not "*have_a_not+"both "+var2+" and "+var1
	if len(var_str.split("either "))>1:
		var1 = var_str.split("either ")[1].split(" or ")[0]
		var2 = var_str.split("either ")[1].split(" or ")[1]
		return "not "*have_a_not+"either "+var2+" or "+var1
	return "not "*have_a_not+var_str
	
def de_morgan(var_str):
	var_split = var_str.split(" ")
	if len(var_split) <= 2:
		return var_str
	if var_split[0] == "not":
		return negate_var(" ".join(var_split[1:]))
	else:
		return "not "+negate_var(var_str)
	return

def gen_same(prompt):
	# prompt: in the form of "If X then Y"
	# for each prompt, we have three levels of difficulties for "same":
	# 1. exchanging the position of vars enclosed by "either" or "both"
	# 2. de Morgan's law
	# 3. modus tollens
	var_str = {}
	var_str[1] = prompt.split("If ")[1].split(" then ")[0]
	var_str[2] = prompt.split("If ")[1].split(" then ")[1]
	two_vars = 1 if len(var_str[2].split(" "))<=2 else 2
	
	tier1 = "If "+exchange_position(var_str[1])+" then "+exchange_position(var_str[2])
	# print(tier1)
	
	
	tier2 = "If "+de_morgan(var_str[1])+" then "+de_morgan(var_str[2])
	# print(tier2)
	
	tier3 = "If "+negate_var(var_str[2])+" then "+negate_var(var_str[1])
	# print(tier3)
	
	return tier1, tier2, tier3
	
def make_diff(same, to_negate):
	# same: in the form of "If X then Y"
	# if we negate one side of the "same" statement, it's definitely inconsistent with the prompt
	# to_negate: 0 or 1
	var_str = {}
	var_str[1] = same.split("If ")[1].split(" then ")[0]
	var_str[2] = same.split("If ")[1].split(" then ")[1]
	var_str[to_negate+1] = negate_var(var_str[to_negate+1])
	return "If "+var_str[1]+" then "+var_str[2]
	
def find_max_negate(statements):
	return max([len(ss.split("not"))-1 for ss in statements])

def gen_statements(vars_lists):
	connectives = [("both","and"), ("either","or")]
	two_vars_on_left = [1,0]
	negate_connectives = [1,0]
	negate_vars = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]
	all_statements = []
	the_df = pd.DataFrame(columns=["type","type_id","prompt","same","diff","batch","difficulty_tier","max_negate","negate_connective", "connectives", "perm"])
	type_id = 0
	for vars in vars_lists:
		for cc in connectives:
			for nc in negate_connectives:
				var_str = cc[0]+" %s%s "+cc[1]+" %s%s"
				var_str = "not "*nc+var_str
				
				for tvol in two_vars_on_left:
					struct = "If %s then %s"
					struct = struct%(var_str, "%s%s") if tvol else struct%("%s%s", var_str)
					# if not nc:
						# print(struct)
					for perm in permutations(vars):
						for nv in negate_vars:
							prompt = struct%("not "*nv[0], perm[0], "not "*nv[1], perm[1], "not "*nv[2], perm[2])
							all_statements += [struct]
							for ii,same in enumerate(gen_same(prompt)):
								all_statements += [same]
								diff = make_diff(same, type_id%2)
								to_add = {"type":"logic", "type_id":type_id, "prompt":prompt, "same":same, "diff":diff, "difficulty_tier":ii+1, "max_negate":find_max_negate([prompt, same, diff]), "negate_connective":nc, "connectives":cc[1], "perm":perm}
								the_df = the_df.append(to_add, ignore_index=True)
								print(prompt)
								print(same)
								print(diff)
								print()
								type_id += 1
	the_df.to_excel("localizer_roster_logic.xlsx", index=False)				
	return

# print(negate_var("not both X and not Y"))
# print(exchange_position("not either not X or Y"))
# print(de_morgan("both X and Y"))
# gen_same("If X then either not Z or Y")
gen_statements([["X","Y","Z"],["A","B","C"],["P","Q","R"],["L","M","N"]])
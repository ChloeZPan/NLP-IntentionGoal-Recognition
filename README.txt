Project2
------------------------------
Name: Zeyi Pan
Student ID: 31633987
Email: zpan12@ur.rochester.edu

------------------------------
Algorithm recognize_intent
input: observations
output: goals which is a list of list

for observation in observations do
	initialize an empty list: plan_list
	get the types of words in observation
	for plan in plan_library do
		for act in each plan’s act
			match the words in observation with words in act
			if all match
				store plan’s goal in plan_list
				replace type in goal to words
	
	update goal_list based on all observations we have for now
	
return goals with minimum cost (which is a list with min length)

Specifically, in step “update goal_list”, suppose our existing goal list is [goal1, goal2], the current plan_list is [goal1, goal3]. The possible goals will be [[goal1], [goal2, goal3]].

To achieve this, we need to check if a goal exists in both lists. Then, combine those which don’t appear twice. Also, I use set() to remove duplicate goals (for example, when combine [goal2, goal3] and [goal2]).

I also write an auxiliary method.
--------------------------------
Algorithm match_type
input: observation, act, plan_list

for goals in plan_list
	for goal in goals
		if second type of act is equal to second type in goal then
			replace second type in goal with second word in observation
		if third type of act is equal to third type in goal then
			replace third type in goal with third word in observation


	
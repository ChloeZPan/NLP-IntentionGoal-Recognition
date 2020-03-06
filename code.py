import json
from pytrips import ontology

ont = ontology.load()
"""
The skeleton file. You should implement your code here. Make sure that the code you write here runs properly
when called by the test.py file in the root directory.

Feel free to add any import statements above, AS LONG AS the package is jsontrips, pytrips, or any
package in the Python standard library.

Feel free to write any additional functions you need in this file, but DO NOT create any new Python files.
"""


def match_type(obs, act, p_list):
    for i in p_list:
        for j in range(len(i)):
            if act[1] == i[j][1]:
                i[j] = (
                    i[j][0],
                    obs[1],
                    i[j][2])
            if act[2] == i[j][2]:
                i[j] = (
                    i[j][0],
                    i[j][1],
                    obs[2])


def recognize_intent(observations):
    """Takes observations as input: this is a list of tuples of the form (word1, word2, word3), where each
     tuple represents an observation (listed in order of occurrence). Return a list of lists (interpreted as
     described in the guidelines), e.g. [[('ONT::STEAL', 'partner', 'store'), ('ONT::TARGET_PRACTICE', 'person', 'gun')]]"""

    plan_library = read_plan_library()  # Read plan library from files in input/plan_libraries

    # TODO: IMPLEMENT FUNCTION HERE
    goals_list = []
    for obs in observations:
        plan_list = []
        types_0 = ont['w::' + obs[0]]
        types_1 = ont['w::' + obs[1]]
        types_2 = ont['w::' + obs[2]]
        for plan in plan_library:
            for act in plan['acts']:
                for t0 in types_0:
                    if t0 == ont[act[0]] or t0 < ont[act[0]]:
                        flag0 = True
                        break
                    else:
                        flag0 = False
                for t1 in types_1:
                    if t1 == ont[act[1][3:]] or t1 < ont[act[1][3:]]:
                        flag1 = True
                        break
                    else:
                        flag1 = False
                for t2 in types_2:
                    if t2 == ont[act[2][3:]] or t2 < ont[act[2][3:]]:
                        flag2 = True
                        break
                    else:
                        flag2 = False
                if flag0 & flag1 & flag2:
                    plan_list.append([plan['goal']])
                    match_type(obs, act, plan_list)
                    match_type(obs, act, goals_list)

        if len(goals_list) > 0:
            for i in range(len(goals_list)):
                for j in plan_list:
                    if goals_list[i] != j:
                        goals_list[i] = list(set(goals_list[i] + j))
        else:
            goals_list = plan_list

    min_cost = min(len(x) for x in goals_list)
    goals = []
    for g in goals_list:
        if len(g) == min_cost:
            goals.append(g)

    return goals


def parse_tuple_string(str):
    """Parses a string representing a tuple into a tuple of strings."""
    strs = str.strip().strip('(').strip(')').split()
    return (strs[0].lower(), strs[1].lower(), strs[2].lower())


def list_tuple_string(st):
    """Parses a string representing a tuple into list of a tuple of strings. """
    strs = st.strip().strip('(').strip(')').split()
    l = []
    l.append((strs[0].lower(), strs[1].lower(), strs[2].lower()))
    return l


def read_plan_library():
    """Reads in plan library from plan library files."""
    # Define file paths to load from
    plan_library_test = 'input/plan_libraries/plan_library_test.json'
    plan_library_custom = 'input/plan_libraries/plan_library_custom.json'
    plan_library = []
    # Read test plan library
    with open(plan_library_test) as f:
        plans_test = json.load(f)
        plan_library += [{'goal': parse_tuple_string(plan['goal']),
                          'acts': list(map(parse_tuple_string, plan['acts']))} for plan in plans_test]
    # Read custom plan library
    with open(plan_library_custom) as f:
        plans_custom = json.load(f)
        plan_library += [{'goal': parse_tuple_string(plan['goal']),
                          'acts': list(map(parse_tuple_string, plan['acts']))} for plan in plans_custom]
    return plan_library

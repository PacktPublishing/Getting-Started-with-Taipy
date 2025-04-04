import taipy as tp


# Updater for the selector page:
def update_compare_selector(state):
    all_tags = [scenario.tags for scenario in tp.get_scenarios()]
    all_tag_set = set()
    for tag in all_tags:
        all_tag_set.update(tag)
    all_park_scenario = [
        tag.replace("park: ", "") for tag in all_tag_set if "park: " in tag
    ]
    state.scenarios_to_compare = all_park_scenario

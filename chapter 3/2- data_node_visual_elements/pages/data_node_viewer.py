import taipy.gui.builder as tgb
from orchestration import biggest_cities

with tgb.Page() as data_node_viewer:
    tgb.text("## Discovering Data Node viewers", mode="md")

    tgb.data_node(
        data_node="{biggest_cities}",
        show_config=True,
        show_owner=True,  # Default is True anyhow
        show_edit_date=True,
        show_expiration_date=True,
        show_properties=True,  # Default is True anyhow
        show_history=True,  # Default is True anyhow
        show_data=True,  # Default is True anyhow
        show_owner_label=True,
    )

import taipy as tp
from taipy import Config, Orchestrator, Scope

## Configure an In-Memory Data Node ##


tokyo_in_memory_node_config = Config.configure_in_memory_data_node(
    id="tokyo_data_node",
    default_data="Tokyo",
    scope=Scope.GLOBAL,
)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()

    tokyo_in_memory_data_node = tp.create_global_data_node(tokyo_in_memory_node_config)
    tokyo = tokyo_in_memory_data_node.read()
    print(
        """Data from a declarative object stored in memory
        (biggest city in the world):"""
    )
    print(tokyo)

    orchestrator.stop()

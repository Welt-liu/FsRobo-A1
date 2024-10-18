from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_spawn_controllers_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("test_arm_1018_new_new", package_name="this_is_new_moveit2").to_moveit_configs()
    return generate_spawn_controllers_launch(moveit_config)

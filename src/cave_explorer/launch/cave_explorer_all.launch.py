"""
Convenience launch file that brings up everything (simulator + RViz, SLAM + Nav2,
and the autonomy node) with a single command, instead of needing three separate
terminals. It just includes the three existing launch files, so it stays in sync
with them automatically; run 'ros2 launch cave_explorer cave_explorer_all.launch.py --show-args'
to see the full set of forwarded arguments.

If you're actively iterating on your own code, you may still prefer the three
separate launch files (see the README) - it lets you restart SLAM/Nav2/autonomy
without restarting Gazebo, which is the slowest part to start up.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    ld = LaunchDescription()
    launch_path = [FindPackageShare('cave_explorer'), 'launch']

    # Additional command line arguments (forwarded to the three launch files below)
    use_sim_time_launch_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Flag to enable use_sim_time'
    )
    world_launch_arg = DeclareLaunchArgument(
        'world',
        default_value='mars_cave.sdf',
        description='Which world to load',
        choices=['mars_cave.sdf', 'mars_surface.sdf']
    )
    odom_mode_launch_arg = DeclareLaunchArgument(
        'odom_mode',
        default_value='robot_localization',
        description='How to publish odom -> base_link transform',
        choices=['gazebo', 'robot_localization']
    )
    depth_pointcloud_launch_arg = DeclareLaunchArgument(
        'depth_pointcloud',
        default_value='False',
        description='Flag to bridge the 3D pointcloud from the RGB-D camera'
    )
    print_feedback_launch_arg = DeclareLaunchArgument(
        'print_feedback',
        default_value='False',
        description='Flag to enable print feedback from action server'
    )
    dataset_dir_launch_arg = DeclareLaunchArgument(
        'dataset_dir',
        default_value='',
        description='Perception 1: directory to save dataset images to. Leave empty to disable.'
    )
    dataset_save_period_launch_arg = DeclareLaunchArgument(
        'dataset_save_period',
        default_value='2.0',
        description='Perception 1: minimum seconds between automatically saved dataset images'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    startup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(launch_path + ['cave_explorer_startup.launch.py'])),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'world': LaunchConfiguration('world'),
            'odom_mode': LaunchConfiguration('odom_mode'),
            'depth_pointcloud': LaunchConfiguration('depth_pointcloud'),
        }.items()
    )

    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(launch_path + ['cave_explorer_navigation.launch.py'])),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items()
    )

    autonomy = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(launch_path + ['cave_explorer_autonomy.launch.py'])),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'print_feedback': LaunchConfiguration('print_feedback'),
            'dataset_dir': LaunchConfiguration('dataset_dir'),
            'dataset_save_period': LaunchConfiguration('dataset_save_period'),
        }.items()
    )

    ld.add_action(use_sim_time_launch_arg)
    ld.add_action(world_launch_arg)
    ld.add_action(odom_mode_launch_arg)
    ld.add_action(depth_pointcloud_launch_arg)
    ld.add_action(print_feedback_launch_arg)
    ld.add_action(dataset_dir_launch_arg)
    ld.add_action(dataset_save_period_launch_arg)

    ld.add_action(startup)
    ld.add_action(navigation)
    ld.add_action(autonomy)

    return ld

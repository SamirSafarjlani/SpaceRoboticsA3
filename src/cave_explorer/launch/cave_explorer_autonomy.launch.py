
import launch_ros.actions
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import (Command, LaunchConfiguration,
                                  PathJoinSubstitution)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    ld = LaunchDescription()
    config_path = [FindPackageShare('cave_explorer'), 'config']
    
    # Additional command line arguments
    use_sim_time_launch_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Flag to enable use_sim_time'
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

    # Start Navigation Stack
    cave_explorer_node = Node(
        package='cave_explorer',
        executable='cave_explorer',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time'),
                     'print_feedback': LaunchConfiguration('print_feedback'),
                     'dataset_dir': LaunchConfiguration('dataset_dir'),
                     'dataset_save_period': LaunchConfiguration('dataset_save_period'),
                    'computer_vision_model_filename': PathJoinSubstitution(config_path+['stop_data.xml'])}]
    )

    ld.add_action(use_sim_time_launch_arg)
    ld.add_action(print_feedback_launch_arg)
    ld.add_action(dataset_dir_launch_arg)
    ld.add_action(dataset_save_period_launch_arg)
    ld.add_action(cave_explorer_node)

    return ld
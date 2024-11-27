from setuptools import find_packages, setup

package_name = 'robo_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='1994524450@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller = robo_controller.robo_controller:main',
            'tech = robo_controller.tech_mode_controller:main',
            'keyboard = robo_controller.keyboard_controller:main',
            'rviz_gui_controller = robo_controller.rviz_gui_controller:main'
            'kdl_kinematics_control_node = robo_controller.kdl_kinematics_control_node:main',  
        ],
    },
)

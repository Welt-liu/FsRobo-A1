from setuptools import find_packages, setup

package_name = 'robo_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ny',
    maintainer_email='1994524450@qq.com',
    description='Examples of FsRobo_A1',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'follower = robo_driver.robo_follower_node:main',
            'leader = robo_driver.robo_leader_node:main',
            'driver = robo_driver.robo_arm_control_node:main',
            'keyboard = robo_driver.keyboard_control_node.py:main'
        ],
    },
)

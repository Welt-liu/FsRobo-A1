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
            'follower = robo_driver.fsrobo_a1_follower:main',
            'leader = robo_driver.fsrobo_a1_leader:main',
            'driver = robo_driver.fsrobo_a1_driver:main'
        ],
    },
)

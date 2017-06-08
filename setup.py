from setuptools import setup

setup(
    name="time-tests",
    version="0.0.1",
    url="https://github.com/andiwand/time-tests",
    license="GNU Lesser General Public License",
    author="Andreas Stefl",
    install_requires=["wiringpi"],
    author_email="stefl.andreas@gmail.com",
    description="time test scripts",
    long_description="",
    package_dir={"": "src"},
    packages=["timetests", "timetests.delay", "timetests.tvt"],
    platforms=["linux"],
    entry_points={
        "console_scripts": [
            "delay-plot = timetests.delay.plot:main",
            "delay-icmp = timetests.delay.icmp:main",
            "delay-gpio = timetests.delay.gpio:main",
            "delay-nmea = timetests.delay.nmea:main",
            "delay-system = timetests.delay.system:main",
            "tvt-plot = timetests.tvt.plot:main",
            "tvt-udp-client = timetests.tvt.udp_client:main",
            "tvt-udp-server = timetests.tvt.udp_server:main",
            "tvt-gpio-client = timetests.tvt.gpio_client:main",
            "tvt-gpio-server = timetests.tvt.gpio_server:main",
        ]
    },
)

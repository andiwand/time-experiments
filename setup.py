from setuptools import setup

setup(
    name="time-tests",
    version="0.0.1",
    url="https://github.com/andiwand/time-experiments",
    license="GNU Lesser General Public License",
    author="Andreas Stefl",
    install_requires=["wiringpi"],
    author_email="stefl.andreas@gmail.com",
    description="time experiment scripts",
    long_description="",
    package_dir={"": "src"},
    packages=["timeexperiments", "timeexperiments.delay", "timeexperiments.tvt"],
    platforms=["linux"],
    entry_points={
        "console_scripts": [
            "delay-icmp = timeexperiments.delay.icmp:main",
            "delay-gpio = timeexperiments.delay.gpio:main",
            "delay-nmea = timeexperiments.delay.nmea:main",
            "delay-system = timeexperiments.delay.system:main",
            "tvt-udp-client = timeexperiments.tvt.udp_client:main",
            "tvt-udp-server = timeexperiments.tvt.udp_server:main",
            "tvt-gpio-client = timeexperiments.tvt.gpio_client:main",
            "tvt-gpio-server = timeexperiments.tvt.gpio_server:main"
        ]
    },
)

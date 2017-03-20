from distutils.core import setup

setup(
    name="time-tests",
    version="0.0.1",
    url="https://github.com/andiwand/time-tests",
    license="GNU Lesser General Public License",
    author="Andreas Stefl",
    install_requires=[],
    author_email="stefl.andreas@gmail.com",
    description="time test scripts",
    long_description="",
    package_dir={"": "src"},
    packages=["delay", "tvt"],
    platforms=["linux"],
    entry_points={
        "console_scripts": [
            "delay-plot = delay.plot:main",
            "delay-icmp = delay.icmp:main",
            "delay-gpio = delay.gpio:main",
            "delay-system = delay.system:main",
            "tvt-plot = tvt.plot:main",
            "tvt-udp-client = tvt.udp_client:main",
            "tvt-udp-server = tvt.udp_server:main",
            "tvt-gpio-client = tvt.gpio_client:main",
            "tvt-gpio-server = tvt.gpio_server:main",
        ]
    },
)

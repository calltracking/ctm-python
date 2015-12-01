from setuptools import setup
import sys

requires = ['requests>=0.10.8']
if sys.version_info < (2, 6):
    requires.append('simplejson')

setup(
    name = "ctm",
    py_modules = ['ctm'],
    version = "0.11.0",
    description = "CallTrackingMetrics Python library",
    author = "CallTrackingMetrics Team",
    author_email = "info@calltrackingmetrics.com",
    url = "https://github.com/calltracking/ctm-python",
    keywords = ["call tracking", "rest"],
    install_requires = requires,
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony"
        ],
    long_description = """\
        CallTrackingMetrics Python library
         """ )

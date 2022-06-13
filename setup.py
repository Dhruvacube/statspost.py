import re

from setuptools import setup

pakage_name = 'botlist_statspost'
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open(f'{pakage_name}/__init__.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

if version.endswith(('a', 'b', 'rc')):
    # append version identifier based on commit count
    try:
        import subprocess
        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass

readme = ''
with open('README.rst') as f:
    readme = f.read()

extras_require = {
    'speed': [
        "aiohttp[speedups]>=3.8.1"
    ],
    'docs': [
        'sphinx',
        'sphinxcontrib_trio',
        'sphinxcontrib-websupport',
        'sphinx-autoapi',
        'typing-extensions'
    ],
    'discord': [
        "discord.py>=1.7.3"
    ]

}

packages = [
    pakage_name,
]

setup(
    name=f'{pakage_name}.py',
    author='Dhruva Shaw',
    url='https://github.com/The-4th-Hokage/botlist-statspost',
    project_urls={
        "Documentation": "https://bluedocs.page/fluxpoint-api",
        "Issue tracker": "https://github.com/The-4th-Hokage/botlist-statspost/issues",
    },
    version=version,
    packages=packages,
    license='MIT',
    description='A Python wrapper for the Fluxpoint API',
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    package_data={pakage_name: ["py.typed"]},
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)

from io import open

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='colorlabels',
    version='0.5.2',
    description='Provides colorful and semantic labels in console. Tailored for message display and interaction in automated scripts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gousaiyang/colorlabels',
    author='Saiyang Gou',
    author_email='gousaiyang223@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: System :: Logging',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
    keywords='console terminal color message display animation progress progressbar',
    py_modules=['colorlabels'],
    install_requires=['colorama;platform_system=="Windows"'],
)

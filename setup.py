from setuptools import setup

setup(
    name='colorlabels',
    version='0.5.0',
    description='Provides colorful and semantic labels in console. Tailored for message display and interaction in automated scripts.',
    long_description='For more information, goto https://github.com/gousaiyang/colorlabels.',
    url='https://github.com/gousaiyang/colorlabels',
    author='Saiyang Gou',
    author_email='gousaiyang223@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='console color display animation',
    py_modules=['colorlabels'],
    install_requires=['colorama'],
)

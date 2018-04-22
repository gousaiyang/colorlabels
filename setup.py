from distutils.core import setup

setup(
    name='colorlabels',
    version='0.1.1',
    description='Provides awesome colorful labels in console. Designed for message display and interaction in automated scripts.',
    long_description='For more information, goto [the Github README page](https://github.com/gousaiyang/colorlabels).',
    long_description_content_type='text/markdown',
    url='https://github.com/gousaiyang/colorlabels',
    author = 'Saiyang Gou',
    author_email = 'gousaiyang223@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
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

from setuptools import setup, find_packages

setup(
    name='GuiFramework',
    version='0.1.0',
    packages=find_packages(),
    description='A Framework build on customtkinter to create GUIs with more ease.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='JanPanthera',
    author_email='JanPanthera@outlook.de',
    url='https://github.com/JanPanthera/_GuiFramework',
    install_requires=[
        'customtkinter',
        'babel',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

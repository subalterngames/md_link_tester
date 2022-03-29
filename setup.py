from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='md_link_tester',
    version="1.1.1",
    description='High-level API for the Magnebot in TDW.',
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/alters-mit/md_link_tester',
    author='Seth Alter',
    author_email="alters@mit.edu",
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords=["documentation", "doc", "sphinx", "markdown", "github"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests']
)

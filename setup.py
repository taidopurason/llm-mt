from setuptools import setup, find_packages

setup(
    name='llm_mt_eval',
    version='0.1.0',
    packages=find_packages(),
    url='',
    license='',
    author='',
    author_email='',
    description='',
    install_requires=[
        "numpy",
        "pandas",
        "openai",
        "tiktoken",
        "tenacity",
        "sacrebleu==2.3.1",
    ]
)
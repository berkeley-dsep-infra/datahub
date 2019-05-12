from setuptools import setup, find_packages

setup(
    name='jupyterhub-sparklykubespawner',
    version='0.1dev',
    python_requires='>=3.5',
    packages=find_packages(),
    install_requires=[
        'google-cloud-storage',
        'google-cloud-iam',
        'google-api-python-client',
    ]
)

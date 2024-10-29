from setuptools import setup

try:
    import pypandoc

    long_description = pypandoc.convert_file("README.md", "rst")
except (IOError, ImportError):
    long_description = open("README.md").read()

setup(
    url="https://github.com/HosseinSayyedMousavi/django-ticket",
    name="django-ticket",
    version="2.1.2",
    description="A ticket application for Django projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Hossein Sayyedmousavi",
    maintainer_email="Hossein.Sayyedmousavi@gmail.com",
    author="Abbas Ebadian",
    author_email="AbbasEbadiann@gmail.com",
    keywords=[
        "django",
        "database",
        "ticket",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Environment :: Console",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Database",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Compression",
    ],
    packages=["ticket"],
    install_requires=[
        "django",
        "djangorestframework"
    ]
)

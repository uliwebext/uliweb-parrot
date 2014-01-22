from uliweb.utils.setup import setup
import parrot

setup(name='parrot',
    version=parrot.__version__,
    description="OAuth2.0 client for uliweb",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    packages = ['parrot'],
    platforms = 'any',
    keywords='oauth2 oauth web framework',
    author=parrot.__author__,
    author_email=parrot.__author_email__,
    url=parrot.__url__,
    license=parrot.__license__,
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'uliweb_apps': [
          'helpers = parrot',
        ],
    },
)

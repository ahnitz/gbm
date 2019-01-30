#!/usr/bin/env python

# Copyright (C) 2019 Alex Nitz
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import setuptools

install_requires = ["numpy",
                    "astropy",
                   ]
setuptools.setup(
    name="gbm",
    version="0.0.1",
    author="Alexander Harvey Nitz",
    author_email="alex.nitz@gmail.com",
    description="Read and analyze GBM data",
    url="https://github.com/ahnitz/gbm",
    install_requires = install_requires,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
    ],
)

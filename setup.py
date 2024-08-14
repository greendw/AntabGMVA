from setuptools import setup

setup(name='antabgmva',
      version='24.813',
      description='A Python tool for managing GMVA metadata',
      url='https://github.com/greendw/AntabGMVA',
      author='Daewon Kim',
      author_email='dwkimastro@gmail.com',
      license='GPLv3',
      packages=['antabgmva'],
      keywords = 'VLBI observation ANTAB Tsys calibration',
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',     
          'Intended Audience :: Developers',    
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.8',
      ],
      )


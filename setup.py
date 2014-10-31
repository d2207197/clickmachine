from distutils.core import setup
setup(name='clickmachine',
      version='0.0.1',
      url='https://github.com/d2207197/clickmachine',
      packages=['clickmachine'],
      package_dir={'clickmachine': 'clickmachine'},
      scripts = ['tools/simple_click'],
      requires = [
          'PyUserInput (>=0.1.9)'
      ]
)


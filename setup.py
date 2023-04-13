from setuptools import setup, find_packages
import codecs
import os
import platform


# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
try:
  with codecs.open(os.path.join(here, 'READMEPACKAGE.md'), encoding='utf-8') as f:
      long_description = f.read()
except:
  # This happens when running tests
  long_description = None

# TODO test if good

setup(name='sema-tc',
      version='0.1',
      description='SEMA: ToolChain for Malware Analysis',
      long_description=long_description,
      url='https://github.com/csvl/SEMA-ToolChain/tree/production',
      author='A-Team from UCLouvain',
      author_email='nomail@uclouvain.com',
      license='MIT', 
      packages=find_packages(),
      package_data={
        'src': [
          'SemaSCDG/procedures/calls/*.json',
          'SemaClassifier/classifier/saved_model/*.pkl',
          'SemaClassifier/classifier/SVM/dico/*.pkl',
          "submodules/*"
        ],
      },
      setup_requires=['wheel'],
      install_requires=[
          'pymongo', # malwexp
          'pyzipper',  
          'click==8.0.3', # for task (8.0.3) 7.1.2
          'task',
          'requests',
          'graphviz',
          'monkeyhex',
          "protobuf==3.20.*",
          'angr==9.2.21', # 8.20.7.27 for symbion (not working after) 9.2.21 -> no present in pypy
          'researchpy',
          'hypothesis',
          'seaborn',
          'scipy',
          'scikit-learn', #'sklearn',
          'grakel',
          # 'torch',
          # 'torchvision',
          'gensim',
          'avatar2',
          'r2pipe',
          'pyinstaller',
          'matplotlib',
          'celery', # ==4.4.7
          'tenseal',
          'dill',
          'cryptography',
          'logbook',
          'mmh3',
          'psutil'
          'claripy',
          "unix",
          'kvm',
          'libvirt-python',
          'unipacker',
          "minidump==0.0.10"
      ],
      zip_safe=False)

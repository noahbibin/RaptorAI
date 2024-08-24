from setuptools import setup, find_packages

setup(
    name='RAPTOR',
    version='0.1.0',
    description='RAPTOR AI is an intelligent object detection system designed to enhance safety by identifying potentially hazardous items in real-time. It offers reliable monitoring for various environments, making it an essential tool for maintaining security.',
    author='Noah Bibin Markose',
    author_email='noahbibin@outlook.com',  # Update with your email
    packages=find_packages(),
    install_requires=[
        'torch',
        'opencv-python',
        'numpy',
        'pygame',
        'PyQt5',
        'pillow',
    ],
    include_package_data=True,
    package_data={
        'raptor': ['assets/alarm.wav', 'assets/RaptorAIsplashscreen.jpg', 'assets/window_icon.png'],
    },
    entry_points={
        'console_scripts': [
            'raptor=raptor.main:main',  # Adjust based on your main entry point
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

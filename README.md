# FLAM
To run FLAM, it is important the perform the installation steps below IN ORDER.

* Install ARGoS: https://github.com/ilpincy/argos3

* Install the Khepera IV ARGoS plugin: https://github.com/ilpincy/argos3-kheperaiv

* Compile the C++ controller:

```bash
cd /FLAM/src/controller
mkdir build
cd build/
cmake ../src
make
sudo make install
```

* Compile the ARGoS loop functions:

```bash
cd FLAM/src/loop_functions
mkdir build
cd build/
cmake ../src
make
sudo make install
```


* Run the experiment with ARGoS:

```bash
cd FLAM/src
make
argos3 -c flam.argos
```

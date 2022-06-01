# FLAM

To run FLAM, it is important the perform the installation steps below IN ORDER.

* Install ARGoS: https://github.com/ilpincy/argos3

* Install the Khepera IV ARGoS plugin: https://github.com/ilpincy/argos3-kheperaiv

* Compile the C++ controller and ARGoS loop functions:

```bash
cmake -Bbuild .
cd build/
make
```
* Run the experiment with ARGoS:

```bash
make
argos3 -c flam.argos
```
